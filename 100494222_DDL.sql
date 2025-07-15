
DROP SCHEMA IF EXISTS cmps_schema CASCADE;
CREATE SCHEMA cmps_schema;
SET search_path TO cmps_schema;

DROP TABLE IF EXISTS cancel CASCADE;
DROP TABLE IF EXISTS entry CASCADE;
DROP TABLE IF EXISTS exam CASCADE;
DROP TABLE IF EXISTS student CASCADE;

CREATE TABLE student (
    sno SERIAL PRIMARY KEY,
    sname VARCHAR(200) NOT NULL,
    semail VARCHAR(200) UNIQUE NOT NULL CHECK (semail LIKE '%@%')
);

CREATE TABLE exam (
    excode CHAR(4) PRIMARY KEY,
    extitle VARCHAR(200) UNIQUE NOT NULL,
    exlocation VARCHAR(200) NOT NULL,
    exdate DATE NOT NULL CHECK (exdate >= '2025-11-01'),
    extime TIME NOT NULL CHECK (extime BETWEEN '09:00' AND '18:00')
);

CREATE TABLE entry (
    eno SERIAL PRIMARY KEY,
    excode CHAR(4) REFERENCES exam(excode),
    sno INTEGER REFERENCES student(sno) ON DELETE CASCADE,
    egrade DECIMAL(5,2) CHECK (egrade BETWEEN 0 AND 100 OR egrade IS NULL),
    UNIQUE (sno, excode)
);

CREATE OR REPLACE FUNCTION prevent_same_day_exam()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM cmps_schema.entry e
        JOIN cmps_schema.exam ex ON e.excode = ex.excode
        WHERE e.sno = NEW.sno
        AND ex.exdate = (SELECT exdate FROM cmps_schema.exam WHERE excode = NEW.excode)
    ) THEN
        RAISE EXCEPTION 'Student is already registered for another exam on this date!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_same_day_exam
BEFORE INSERT ON cmps_schema.entry
FOR EACH ROW
EXECUTE FUNCTION prevent_same_day_exam();

CREATE TABLE cancel (
    eno INTEGER REFERENCES entry(eno) ON DELETE CASCADE,
    excode CHAR(4) NOT NULL,
    sno INTEGER NOT NULL,
    cdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cuser VARCHAR(200) NOT NULL,
    PRIMARY KEY (eno, excode, sno),
    CONSTRAINT cancel_entry_fk FOREIGN KEY (eno) REFERENCES entry(eno) ON DELETE CASCADE
);
