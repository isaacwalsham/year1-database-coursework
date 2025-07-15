
SET search_path TO cmps_schema;

INSERT INTO student (sname, semail) VALUES 
('Percival Hargreaves', 'percival.hargreaves@gmail.com'),
('Gwendolyn Fairchild', 'gwen.fairchild@icloud.com'),
('Benedict Holloway', 'benedict.holloway@yahoo.com'),
('Eleanor Whitmore', 'eleanor.whitmore@outlook.com'),
('Thaddeus Winslow', 'thad.winslow@hotmail.com'),
('Imogen Pembroke', 'imogen.pembroke@gmail.com'),
('Rupert Ellington', 'rupert.ellington@yahoo.com'),
('Beatrix Hastings', 'beatrix.hastings@icloud.com'),
('Cedric Montague', 'cedric.montague@outlook.com'),
('Constance Everly', 'constance.everly@gmail.com');

INSERT INTO exam (excode, extitle, exlocation, exdate, extime) VALUES
('CS01', 'Computer Science Fundamentals', 'Cambridge', '2025-11-05', '09:00'),
('DB02', 'Advanced Databases', 'Oxford', '2025-11-07', '11:00'),
('AI03', 'Machine Learning', 'Edinburgh', '2025-11-10', '14:00');

INSERT INTO entry (excode, sno, egrade) VALUES
('CS01', 1, 78),
('DB02', 2, 85),
('AI03', 3, 92);

SELECT s.sname, ex.exlocation, ex.excode, ex.extitle, ex.exdate, ex.extime
FROM cmps_schema.entry e
JOIN cmps_schema.student s ON e.sno = s.sno
JOIN cmps_schema.exam ex ON e.excode = ex.excode
WHERE s.sno = 2
ORDER BY ex.exdate, ex.extime;

SELECT ex.excode, ex.extitle, s.sname, 
       CASE 
           WHEN e.egrade >= 70 THEN 'Distinction'
           WHEN e.egrade >= 50 THEN 'Pass'
           WHEN e.egrade < 50 THEN 'Fail'
           ELSE 'Not Taken'
       END AS result
FROM cmps_schema.entry e
JOIN cmps_schema.student s ON e.sno = s.sno
JOIN cmps_schema.exam ex ON e.excode = ex.excode
ORDER BY ex.excode, s.sname;
