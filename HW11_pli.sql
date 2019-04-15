select Name from HW11_students where CWID = "11461";

select major, count(*) as Number from HW11_majors group by Major;

select Grade, max(frequent) from (select  Grade, count(*) as frequent from HW11_grades group by Grade);

select s.Name, s.CWID, s.Major, g.Course,g.Grade from HW11_students s join (select Student_CWID, Course, Grade from HW11_grades) g where s.CWID = g.Student_CWID  ;

select Name from (HW11_students s join (select Student_CWID, Course, Grade from HW11_grades where Course= "SSW 540") g on s.CWID = g.Student_CWID) where Grade is not null;

create  table "Instructor summary" (
    cwid varchar(10),
    name varchar(20),
    department varchar(10),
    course varchar(10),
    "number of students" int(2)
)

select  i.CWID,i.Name, i.Dept, g.Course,g.Number  from (HW11_instructors i join (select count(*) as Number, Course, Instructor_CWID from HW11_grades group by Course) g on i.CWID = g.Instructor_CWID);

insert into "Instructor summary"(cwid, name, department, course, "number of students" )values(select s.Name, s.CWID, s.Major, g.Course,g.Grade from HW11_students s join (select Student_CWID, Course, Grade from HW11_grades) g where s.CWID = g.Student_CWID)


