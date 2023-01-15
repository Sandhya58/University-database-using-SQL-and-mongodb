import json
import mysql.connector
from datetime import datetime

import pymongo


def allTrue(array):
    for check in array:
        if check == False:
            return False
    return True

def anyTrue(array):
    for check in array:
        if check == True:
            return True
    return False

def anyFalse(array):
    for check in array:
        if check == False:
            return True
    return False

def allFalse(array):
    for check in array:
        if check == True:
            return True
    return False

def Pre_see(ssn,sub,pre,trans):
    prereq,transcript = [],[]
    for p  in pre:
        prereq.append(p)
    for t in trans:
        transcript.append(t)
    found = 0
    status = []
    for p in prereq:
        if ((str(p['dcode'])+' '+str(p['cno'])) == str(sub)):
            found += 1
    if found == 0:
        return True
    else:
        status= []
        for p in prereq:
            if ((str(p['dcode'])+' '+str(p['cno'])) == str(sub)):
                state = 'nill'
                for t in transcript:
                    if ((str(ssn) == str(t['ssn'])) and (str(p['pcode']) == str(t['dcode'])) and (str(p['pno']) == str(t['cno']))):
                        state = 'found'
                        if (t['grade'] == 'A') or (t['grade'] == 'B'):
                            status.append(True)
                        else:
                            status.append(False)
                if state == 'found':
                    pass
                else:
                    status.append(False)
        return allTrue(status)
def stSatPreAorBb(ssn,sname,stu,pre,clas,enro,trans,key):
    student,prereq,classes,enrollment,transcript = [],[],[],[],[]
    for s in stu:
        student.append(s)
    for p in pre:
        prereq.append(p)
    for c in clas:
        classes.append(c)
    for e in enro:
        enrollment.append(e)
    for t in trans:
        transcript.append(t)

    if key == "ssn":
        found = 0
        for s in student:
            if str(s['ssn']) == str(ssn):
                found +=1
        if found>=1:
            status = []
            
            enroll,sub = dict(),[]
            for e in enrollment:
                if str(e['ssn']) == str(ssn):
                    for c in classes:
                        if c['class'] == e['class']:
                            sub.append(str(c['dcode']+' '+str(c['cno'])))
            enroll.update({ssn:sub})
            for ssn,sub in enroll.items():
                visited = []
                for j in sub:
                    if j not in visited:
                        visited.append(j)
                        status.append(Pre_see(ssn,j,prereq,transcript))
            return allTrue(status)
        else:
            return False

def studentSatPreAorB(ssn,sname,stu,pre,clas,enro,trans,key):
    student,prereq,classes,enrollment,transcript = [],[],[],[],[]
    for s in stu:
        student.append(s)
    for p in pre:
        prereq.append(p)
    for c in clas:
        classes.append(c)
    for e in enro:
        enrollment.append(e)
    for t in trans:
        transcript.append(t)

    if key == "ssn":
        status = []
        # Class enrolled by student
        enroll,sub = dict(),[]
        for e in enrollment:
            if str(e['ssn']) == str(ssn):
                for c in classes:
                    if c['class'] == e['class']:
                        sub.append(str(c['dcode']+' '+str(c['cno'])))
        enroll.update({ssn:sub})
        for ssn,sub in enroll.items():
            visited = []
            for j in sub:
                if j not in visited:
                    visited.append(j)
                    status.append(Pre_see(ssn,j,prereq,transcript))
            return allTrue(status)
        else:
            return False
    elif key == "every_ssn":
        allstudents = []
        for s in student:
            # allstudents.append(s['ssn'])
            allstudents.append(studentSatPreAorB(s['ssn'],"null","null",prereq,classes,enrollment,transcript,'ssn'))
        # print(allstudents)
        return allTrue(allstudents)
    elif key == 'cs_ssn':
        cs_students = []
        for s in student:
            if s['major'] == "CS":
                # cs_students.append(s['ssn'])
                cs_students.append(studentSatPreAorB(s['ssn'],"null","null",prereq,classes,enrollment,transcript,'ssn'))
        return allTrue(cs_students)
    elif key == 'prereq_name':
        prereqs,status = [],[]
        for s in student:
            if s['name']==sname:
                ssn = s['ssn']
                # Class enrolled by student
                enroll,sub = dict(),[]
                for e in enrollment:
                    if str(e['ssn']) == str(ssn):
                        for c in classes:
                            if c['class'] == e['class']:
                                sub.append(str(c['dcode']+' '+str(c['cno'])))
                enroll.update({ssn:sub})
                for ssn,sub in enroll.items():
                    for j in sub:
                        status.append(Pre_see(ssn,j,prereq,transcript))
                break
        return anyTrue(status)

def studentNameNotinPrereq(sname,stu,pre,clas,enro,trans):
    student,prereq,classes,enrollment,transcript = [],[],[],[],[]
    for s in stu:
        student.append(s)
    for p in pre:
        prereq.append(p)
    for c in clas:
        classes.append(c)
    for e in enro:
        enrollment.append(e)
    for t in trans:
        transcript.append(t)

    prereqs,status,found = [],[],0
    for s in student:
        if s['name'] == sname:
            found += 1
    if found >= 1:
        for s in student:
            if s['name'] == sname:
                ssn = s['ssn']
                enroll,sub = dict(),[]
                for e in enrollment:
                    if str(e['ssn']) == str(ssn):
                        for c in classes:
                            if c['class'] == e['class']:
                                sub.append(str(c['dcode']+' '+str(c['cno'])))
                enroll.update({ssn:sub})
                # print(enroll)
                for ssn,sub in enroll.items():
                    for j in sub:
                        status.append(Pre_see(ssn,j,prereq,transcript))
                break
        for s in status:
            if s == False:
                return True
        return False

    else:
        return False

def hasPrereq(sub,pre):
    prereq = []
    for p in pre:
        prereq.append(p)
    for p in prereq:
        if ((str(p['dcode'])+' '+str(p['cno'])) == str(sub)):
            return True
        else:
            pass
    return False

def studentGotAorB(ssn,trans):
    transcript = []
    for t in trans:
        transcript.append(t)
    grades,checker = [],[]
    for t in transcript:
        if str(t['ssn']) == str(ssn):
            grades.append(t['grade'])
    for g in grades:
        if g == 'A' or g =='B':
            checker.append(True)
        else:
            checker.append(False)
    return allTrue(checker)

def coursePrereq(cou,pre,clas,key):
    course,prereq,classes = [],[],[]
    for p in pre:
        prereq.append(p)
    for c in cou:
        course.append(c)
    for c in clas:
        classes.append(c)

    if key == 'didnot':
        haspre = []
        for c in course:
            sub = str(c['dcode'])+' '+str(c['cno'])
            haspre.append(hasPrereq(sub,prereq))
        return anyFalse(haspre)
    elif key == "all_have":
        haspre = []
        for c in classes:
            sub= str(c['dcode'])+' '+str(c['cno'])
            haspre.append(hasPrereq(sub,prereq))
        return allTrue(haspre)

def studentProf(pname,major,ssn,smajor,list_class,list_faculty,list_enroll):
    data_j_1_mongo_subquery = list_class.find({},{"_id":0})
    data_j_2_mongo_subquery = list_faculty.find({},{"_id":0})
    data_j_3_mongo_subquery = list_enroll.find({},{"_id":0})
    classes,faculty,enrollment = [],[],[]
    for c in data_j_1_mongo_subquery:
        classes.append(c)

    
    for f in data_j_2_mongo_subquery:
        faculty.append(f)
    #print("student:  ",ssn, " .   ",faculty)
    for e in data_j_3_mongo_subquery:
        enrollment.append(e)

    fcl_ssn = ""
    for f in faculty:
        if pname == f['name']:
            fcl_ssn = f['ssn']
            break
    classestaught = []
    if fcl_ssn:
        for c in classes:
            if c['instr'] == fcl_ssn:
                classestaught.append(c['class'])
        enroll = set()
        if classestaught:
            for ct in classestaught:
                for e in enrollment:
                    if str(ct) == str(e['class']):
                        enroll.add(e['ssn'])
            if enroll:
                for e in enroll:
                    if (str(e) == str(ssn)):
                        if (major == str(smajor)):
                            return True
                        else:
                            return False
                return False
            else:
                return False
        else:
            return False
    else:
        return False

def studentTookCourse(ssn,sname,cname,trans,stu,key):

    transcript,student = [],[]
    for t in trans:
        transcript.append(t)
    for s in stu:
        student.append(s)

    dcode, cno = cname.split()
    if key == "ssn":
        for i in transcript:
            if (ssn == i['ssn'] and ((str(i['cno'])==cno) and (str(i['dcode'])==dcode))):
                return True
            else:
                pass
        return False
    elif key == "sname":
        for i in student:
            if i['name']==sname:
                return studentTookCourse(i['ssn'],"null",cname,transcript,student,'ssn')
            else:
                pass
        return False
    elif key == "all_st_name":
        checkstudent,resstudent = [],[]
        count,s_lenght = 0,0
        for i in student:
            s_lenght+=1
            if i['name'] == sname:
                count+=1
                checkstudent.append(i['ssn'])
        if count == 0:
            return True
        if count == s_lenght:
            for i in checkstudent:
                resstudent.append(studentTookCourse(i,"null",cname,transcript,student,'ssn'))
            if resstudent:
                for i in resstudent:
                    if i == False:
                        return False
                    else:
                        pass
                return True
            else:
                return False

        else:
            return True

def someStudentsGotAorB(trans,stu):
    transcript,student = [],[]
    for t in trans:
        transcript.append(t)
    for s in stu:
        student.append(s)
    visited,studentgrades,status = [],dict(),[]
    if transcript:
        for t in transcript:
            if t['ssn'] not in visited:
                grades = []
                visited.append(t['ssn'])
                for z in transcript:
                    if t['ssn'] == z['ssn']:
                        grades.append(z['grade'])
                studentgrades.update({t['ssn']:grades})
        for ssn,grades in studentgrades.items():
            checker = []
            for g in grades:
                if g == 'A' or g == 'B':
                    checker.append(True)
                else:
                    checker.append(False)
            status.append(allTrue(checker))
        return anyTrue(status)
    else:
        if student:
            return True # Insight after debugging
        else:
            return False

def mysql_t(jdata,tname):
    mydb = mysql.connector.connect
    cols = []
    attr = []
    for data in jdata:
        attr = list(data.keys())
        for col in attr:
            if col not in cols:
                cols.append(col)

    value = []
    data = []
    for data in jdata:
        for Stu_ in cols:
            value.append(str(dict(data).get(Stu_)))
        data.append(list(value))
        value.clear()
    tname = tname
    my_table = "create table if not exists "+tname+" ({0})".format(" text,".join(cols))
    insert_table = "insert into "+tname+" ({0})\
                    data (?{1})".format(",".join(cols), ",?" * (len(cols)-1))
    print("insert has started at " + str(datetime.now()))
    conn = mydb.cursor()

    conn.execute(my_table)
    conn.executemany(insert_table , data)
    data.clear()
    mydb.commit()
    print(""+ str(datetime.now()))
    conn.close()

def studentMajorProf(pname,major,stu,clas,fac,enro,key):
    student,classes,enrollment,faculty = [],[],[],[]
    for s in stu:
        student.append(s)
    for f in fac:
        faculty.append(f)
    for c in clas:
        classes.append(c)
    for e in enro:
        enrollment.append(e)

    fcl_ssn = ""
    for f in faculty:
        if pname == f['name']:
            fcl_ssn = f['ssn']
            break
    classestaught = []
    if fcl_ssn:
        for c in classes:
            if c['instr'] == fcl_ssn:
                classestaught.append(c['class'])
        enroll = set()
        if classestaught:
            for ct in classestaught:
                for e in enrollment:
                    if str(ct) == str(e['class']):
                        enroll.add(e['ssn'])
            if enroll:
                status = []
                for e in enroll:
                    for s in student:
                        if (str(e) == str(s['ssn'])):
                            if (major == s['major']):
                                status.append(True)
                                break
                            else:
                                status.append(False)
                                break
                if key == "all":
                    return allTrue(status)
                elif key == "some":
                    return anyTrue(status)
            else:
                return False 
        else:
            return False 
    else:
        return True 

def studentMjofac(pname,major,stu,clas,fac,enro,key):
    student,classes,enrollment,faculty = [],[],[],[]
    for s in stu:
        student.append(s)
    for f in fac:
        faculty.append(f)
    for c in clas:
        classes.append(c)
    for e in enro:
        enrollment.append(e)

    fcl_ssn = ""
    for f in faculty:
        if pname == f['name']:
            fcl_ssn = f['ssn']
            break
    classestaught = []
    if fcl_ssn:
        for c in classes:
            if c['instr'] == fcl_ssn:
                classestaught.append(c['class'])
        enroll = set()
        if classestaught:
            for ct in classestaught:
                for e in enrollment:
                    if str(ct) == str(e['class']):
                        enroll.add(e['ssn'])
            if enroll:
                status = []
                for e in enroll:
                    for s in student:
                        if (str(e) == str(s['ssn'])):
                            if (major == s['major']):
                                status.append(True)
                                break
                            else:
                                status.append(False)
                                break
                if key == "all":
                    return allTrue(status)
                elif key == "some":
                    return anyTrue(status)
            else:
                return False 
        else:
            return False 
    else:
        return False



def ha3(univDB):
    initial_db = "university_database"
    tables = univDB["tables"]
    department = tables["department"]
    course = tables["course"]
    prereq = tables["prereq"]
    class_ = tables["class"]
    faculty = tables["faculty"]
    student = tables["student"]
    enrollment = tables["enrollment"]
    transcript = tables["transcript"]
    mydb = mysql.connector.connect(
    host= "localhost",
            user= "root",
            password= "your_password",
            database= "university_database"
    )
    conn = mydb.cursor()

    mydbs = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mydbs["university_database"]
    try:

        list_trans = db['transcript']
        list_trans.insert_many(tables['transcript'])
    except:
        pass

    try:
        list_course = db['course']
        list_course.insert_many(tables['course'])
    except:
        pass

    try:
        list_prereq = db['prereq']
        list_prereq.insert_many(tables['prereq'])
    except:
        pass

    try:
        list_enroll = db['enrollment']
        list_enroll.insert_many(tables['enrollment'])
    except:
        pass

    try:
        list_faculty = db['faculty']
        list_faculty.insert_many(tables['faculty'])
    except:
        pass

    try:
        list_student = db['student']
        list_student.insert_many(tables['student'])
    except:
        pass

    try:
        list_class = db['class']
        list_class.insert_many(tables['class'])
    except:
        pass
    t = []
    
    
    # bool_a_sql_subquery = conn.execute("select class from class where dcode='CS' and cno='530'")
    bool_a_mongo_subquery = list_trans.find({},{"_id":0})

    bool_a_1_mongo_subquery = list_student.find({},{"_id":0})
    boolQuery_a = studentTookCourse(82,"null",'CS 530',bool_a_mongo_subquery,bool_a_1_mongo_subquery,'ssn')
    
#-------------------------------------------------------------------------------


    # bool_b_sql_subquery = conn.execute("select ssn from student where name='John Smith'")
    bool_b_mongo_subquery = list_trans.find({},{"_id":0})
    bool_b_1_mongo_subquery = list_student.find({},{"_id":0})
    boolQuery_b = studentTookCourse("null",'John Smith','CS 530',bool_b_mongo_subquery,bool_b_1_mongo_subquery,'sname')
    

#-------------------------------------------------------------------------------
#working
    # bool_c_sql_subquery = conn.execute("select ssn from student where name='John Smith'")
    bool_c_mongo_subquery = list_trans.find({},{"_id":0})
    bool_c_1_mongo_subquery = list_student.find({},{"_id":0})
    boolQuery_c = studentTookCourse("null",'John Smith','CS 530',bool_c_mongo_subquery,bool_c_1_mongo_subquery,'all_st_name') 
#-------------------------------------------------------------------------------
#working
    # bool_d_sql_subquery = conn.execute("select class,dcode,cno from class")
    bool_d_mongo_subquery = list_trans.find({},{"_id":0})
    bool_d_1_mongo_subquery = list_student.find({},{"_id":0})
    bool_d_2_mongo_subquery = list_prereq.find({},{"_id":0})
    bool_d_3_mongo_subquery = list_class.find({},{"_id":0})
    bool_d_4_mongo_subquery = list_enroll.find({},{"_id":0})
    boolQuery_d = stSatPreAorBb(82,"null",bool_d_1_mongo_subquery,bool_d_2_mongo_subquery,bool_d_3_mongo_subquery,bool_d_4_mongo_subquery,bool_d_mongo_subquery,'ssn')
 
#-------------------------------------------------------------------------------
#working
    bool_e_mongo_subquery = list_trans.find({},{"_id":0})
    bool_e_1_mongo_subquery = list_student.find({},{"_id":0})
    bool_e_2_mongo_subquery = list_prereq.find({},{"_id":0})
    bool_e_3_mongo_subquery = list_class.find({},{"_id":0})
    bool_e_4_mongo_subquery = list_enroll.find({},{"_id":0})
    boolQuery_e = studentSatPreAorB("null","null",bool_e_1_mongo_subquery,bool_e_2_mongo_subquery,bool_e_3_mongo_subquery,bool_e_4_mongo_subquery,bool_e_mongo_subquery,'every_ssn')
    
#-------------------------------------------------------------------------------
#working
    bool_f_mongo_subquery = list_trans.find({},{"_id":0})
    bool_f_1_mongo_subquery = list_student.find({},{"_id":0})
    bool_f_2_mongo_subquery = list_prereq.find({},{"_id":0})
    bool_f_3_mongo_subquery = list_class.find({},{"_id":0})
    bool_f_4_mongo_subquery = list_enroll.find({},{"_id":0})
    boolQuery_f = studentSatPreAorB("null","null",bool_f_1_mongo_subquery,bool_f_2_mongo_subquery,bool_f_3_mongo_subquery,bool_f_4_mongo_subquery,bool_f_mongo_subquery,'cs_ssn')
    

#-------------------------------------------------------------------------------
#working
    bool_g_mongo_subquery = list_trans.find({},{"_id":0})
    bool_g_1_mongo_subquery = list_student.find({},{"_id":0})
    bool_g_2_mongo_subquery = list_prereq.find({},{"_id":0})
    bool_g_3_mongo_subquery = list_class.find({},{"_id":0})
    bool_g_4_mongo_subquery = list_enroll.find({},{"_id":0})
    boolQuery_g = studentSatPreAorB("null","John Smith",bool_g_1_mongo_subquery,bool_g_2_mongo_subquery,bool_g_3_mongo_subquery,bool_g_4_mongo_subquery,bool_g_mongo_subquery,'prereq_name')
    
#-------------------------------------------------------------------------------
    #working
    bool_h_sql_subquery = "tbd"
    bool_h_mongo_subquery = list_course.find({},{"_id":0})
    bool_h_1_mongo_subquery = list_prereq.find({},{"_id":0})
    bool_h_2_mongo_subquery = list_class.find({},{"_id":0})
    boolQuery_h = coursePrereq(bool_h_mongo_subquery,bool_h_1_mongo_subquery,bool_h_2_mongo_subquery,'didnot')
    
#-------------------------------------------------------------------------------
    #working
    
    bool_i_sql_subquery = "tbd"
    bool_i_mongo_subquery = list_course.find({},{"_id":0})
    bool_i_1_mongo_subquery = list_prereq.find({},{"_id":0})
    bool_i_2_mongo_subquery = list_class.find({},{"_id":0})
    boolQuery_i = coursePrereq(bool_i_mongo_subquery,bool_i_1_mongo_subquery,bool_i_2_mongo_subquery,'all_have')
   
#-------------------------------------------------------------------------------
    #working
    # bool_j_sql_subquery = conn.execute("select ssn from student")
    # id = bool_j_sql_subquery.fetchall()
    bool_j_1_mongo_subquery = list_student.find({},{"_id":0})
    students = []
    for s in bool_j_1_mongo_subquery:
        students.append(int(s['ssn']))
    #print(students)
    bool_j_mongo_subquery = list_trans.find({},{"_id":0})
    boolQuery_j = someStudentsGotAorB(bool_j_mongo_subquery,students)
    
#-------------------------------------------------------------------------------
    #working
    
    bool_k_mongo_subquery = list_faculty.find({},{"_id":0})
    bool_k_1_mongo_subquery = list_student.find({},{"_id":0})
    bool_k_2_mongo_subquery = list_class.find({},{"_id":0})
    bool_k_3_mongo_subquery = list_enroll.find({},{"_id":0})
    boolQuery_k = studentMajorProf('Brodsky',"CS",bool_k_1_mongo_subquery,bool_k_2_mongo_subquery,bool_k_mongo_subquery,bool_k_3_mongo_subquery,'all') 
   
#-------------------------------------------------------------------------------
    #working
    
    bool_l_mongo_subquery = list_faculty.find({},{"_id":0})
    bool_l_1_mongo_subquery = list_student.find({},{"_id":0})
    bool_l_2_mongo_subquery = list_class.find({},{"_id":0})
    bool_l_3_mongo_subquery = list_enroll.find({},{"_id":0})
    boolQuery_l = studentMjofac('Brodsky',"CS",bool_l_1_mongo_subquery,bool_l_2_mongo_subquery,bool_l_mongo_subquery,bool_l_3_mongo_subquery,'some')
   
#-------------------------------------------------------------------------------
# Data queries
#-------------------------------------------------------------------------------
    # data_a_sql_subquery = conn.execute("select class from class where dcode='CS' and cno='530'")
    data_a_mongo_subquery = list_trans.find({},{"_id":0})
    data_a_1_mongo_subquery = list_student.find({},{"_id":0})
    transcript,student = [],[]
    for t in data_a_mongo_subquery:
        transcript.append(t)
    for s in data_a_1_mongo_subquery:
        student.append(s)

    dataQuery_a = sorted([
    s
    for t in transcript
    if ((str(t['dcode'])+' '+str(t['cno']))=='CS 530')
    for s in student
    if s['ssn'] == t['ssn']
    ], key=lambda x:x['ssn'])


#-------------------------------------------------------------------------------
    # data_b_sql_subquery = conn.execute("select ssn from student where name='John Smith'")
    data_b_mongo_subquery = list_trans.find({},{"_id":0})
    data_b_1_mongo_subquery =list_student.find({},{"_id":0})
    transcript,student = [],[]
    for t in data_b_mongo_subquery:
        transcript.append(t)
    for s in data_b_1_mongo_subquery:
        student.append(s)
    dataQuery_b = sorted([
    s
    for t in transcript
    if ((str(t['dcode'])+' '+str(t['cno']))=='CS 530')
    for s in student
    if (s['ssn'] == t['ssn']) and (s['name']=='John')
    ], key=lambda x:x['ssn'])
    
#-------------------------------------------------------------------------------
    data_c_sql_subquery = "tbd"
    data_c_mongo_subquery = list_trans.find({},{"_id":0})
    data_c_1_mongo_subquery = list_student.find({},{"_id":0})
    data_c_2_mongo_subquery = list_prereq.find({},{"_id":0})
    data_c_3_mongo_subquery = list_class.find({},{"_id":0})
    data_c_4_mongo_subquery = list_enroll.find({},{"_id":0})
    student,prereq,classes,enroll,transcript = [],[],[],[],[]
    for s in data_c_1_mongo_subquery:
        student.append(s)
    for p in data_c_2_mongo_subquery:
        prereq.append(p)
    for c in data_c_3_mongo_subquery:
        classes.append(c)
    for e in data_c_4_mongo_subquery:
        enroll.append(e)
    for t in data_c_mongo_subquery:
        transcript.append(t)

    dataQuery_c = sorted([
    s
    for s in student
    if studentSatPreAorB(s['ssn'],"null","null",prereq,classes,enrollment,transcript,'ssn')
    ], key=lambda x:x['ssn'])
 
#-------------------------------------------------------------------------------
    data_d_sql_subquery = "tbd"
    data_d_mongo_subquery = list_trans.find({},{"_id":0})
    data_d_1_mongo_subquery = list_student.find({},{"_id":0})
    data_d_2_mongo_subquery = list_prereq.find({},{"_id":0})
    data_d_3_mongo_subquery = list_class.find({},{"_id":0})
    data_d_4_mongo_subquery = list_enroll.find({},{"_id":0})
    student,prereq,classes,enroll,transcript = [],[],[],[],[]
    for s in data_d_1_mongo_subquery:
        student.append(s)
    for p in data_d_2_mongo_subquery:
        prereq.append(p)
    for c in data_d_3_mongo_subquery:
        classes.append(c)
    for e in data_d_4_mongo_subquery:
        enroll.append(e)
    for t in data_d_mongo_subquery:
        transcript.append(t)
    dataQuery_d = sorted([
    s
    for s in student
   
    if not studentSatPreAorB(s['ssn'],"null","null",prereq,classes,enrollment,transcript,'ssn')
    ], key=lambda x:x['ssn'])
   
#-------------------------------------------------------------------------------
    data_e_sql_subquery = "tbd"
    data_e_mongo_subquery = list_trans.find({},{"_id":0})
    data_e_1_mongo_subquery = list_student.find({},{"_id":0})
    data_e_2_mongo_subquery = list_prereq.find({},{"_id":0})
    data_e_3_mongo_subquery = list_class.find({},{"_id":0})
    data_e_4_mongo_subquery = list_enroll.find({},{"_id":0})
    student = []
    for s in data_e_2_mongo_subquery:
        student.append(s)
    dataQuery_e = sorted([
    s
    for s in student
    if studentNameNotinPrereq('John',data_e_1_mongo_subquery,data_e_2_mongo_subquery,data_e_3_mongo_subquery,data_e_4_mongo_subquery,data_e_mongo_subquery)
    ], key = lambda x:x['ssn'])
   
#-------------------------------------------------------------------------------
    data_f_sql_subquery = "tbd"
    data_f_mongo_subquery = list_prereq.find({},{"_id":0})
    prereq = []
    for p in data_f_mongo_subquery:
        prereq.append(p)
    dataQuery_f =  sorted([
    {'dcode': sub['dcode'],'cno': sub['cno']}
    for sno,sub in enumerate(tables['course'])
    if not hasPrereq((str(sub['dcode'])+' '+str(sub['cno'])),prereq)
    ], key=lambda x:(x['dcode'],x['cno']))
    
#-------------------------------------------------------------------------------
    data_g_sql_subquery = "tbd"
    data_g_mongo_subquery = list_prereq.find({},{"_id":0})
    prereq = []
    for p in data_g_mongo_subquery:
        prereq.append(p)
    dataQuery_g = sorted([
    {'dcode': sub['dcode'],'cno': sub['cno']}
    for sno,sub in enumerate(tables['course'])
    if hasPrereq((str(sub['dcode'])+' '+str(sub['cno'])),prereq)
    ], key=lambda x:(x['dcode'],x['cno']))
   

#-------------------------------------------------------------------------------

    data_h_mongo_subquery = list_prereq.find({},{"_id":0})
    prereq = []
    for p in data_h_mongo_subquery:
        prereq.append(p)
    dataQuery_h = sorted([
    {'class': classestaught['class'],'dcode':classestaught['dcode'], 'cno':classestaught['cno'] ,'instr':classestaught['instr']}
    for sno,classestaught in enumerate(tables['class'])
    if hasPrereq((str(classestaught['dcode'])+' '+str(classestaught['cno'])),prereq)
    ], key=lambda x:x['class'])
   
#-------------------------------------------------------------------------------
    # data_i_sql_subquery = conn.execute("select ssn from student")
    data_i_mongo_subquery = list_trans.find({},{"_id":0})
    data_i_1_mongo_subquery = list_student.find({},{"_id":0})
    student,transcript = [],[]
    for t in data_i_mongo_subquery:
        transcript.append(t)
    for s in data_i_1_mongo_subquery:
        student.append(s)
    dataQuery_i = sorted([
    s
    for s in student
    if studentGotAorB(s['ssn'],transcript)
    ],key=lambda x:x['ssn'])
   

#-------------------------------------------------------------------------------
    # data_j_sql_subquery = conn.execute("select ssn from student")
    data_j_mongo_subquery = list_student.find({},{"_id":0})
    data_j_1_mongo_subquery = list_class.find({},{"_id":0})
    data_j_2_mongo_subquery = list_faculty.find({},{"_id":0})
    data_j_3_mongo_subquery = list_enroll.find({},{"_id":0})
    student = []
    faculty=[]
    for s in data_j_mongo_subquery:
        student.append(s)
    dataQuery_j = ([
    s
    for s in student
        
        if studentProf('Brodsky','CS',s['ssn'],s['major'],list_class,list_faculty,list_enroll)])
    #print(data_j_1_mongo_subquery[0])
#-------------------------------------------------------------------------------
  
    mydbs.drop_database('university_database')
    conn.execute("DROP TABLE IF EXISTS DEPARTMENT")
    conn.execute("DROP TABLE IF EXISTS STUDENT")
    conn.execute("DROP TABLE IF EXISTS COURSE")






    return({
        "boolQuery_a": boolQuery_a,
        "boolQuery_b": boolQuery_b,
        "boolQuery_c": boolQuery_c,
        "boolQuery_d": boolQuery_d,
        "boolQuery_e": boolQuery_e,
        "boolQuery_f": boolQuery_f,
        "boolQuery_g": boolQuery_g,
        "boolQuery_h": boolQuery_h,
        "boolQuery_i": boolQuery_i,
        "boolQuery_j": boolQuery_j,
        "boolQuery_k": boolQuery_k,
        "boolQuery_l": boolQuery_l,
        "dataQuery_a": dataQuery_a,
        "dataQuery_b": dataQuery_b,
        "dataQuery_c": dataQuery_c,
        "dataQuery_d": dataQuery_d,
        "dataQuery_e": dataQuery_e,
        "dataQuery_f": dataQuery_f,
        "dataQuery_g": dataQuery_g,
        "dataQuery_h": dataQuery_h,
        "dataQuery_i": dataQuery_i,
        "dataQuery_j": dataQuery_j
    })
``