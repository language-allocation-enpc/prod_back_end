import json
from pymongo import MongoClient
from data_structs import *
import random, string
client = MongoClient()

app_db = client.language_allocation_database
app_db.courses.delete_many({})
app_db.creneaux.delete_many({})
app_db.users.delete_many({})

def write_creneau(id=-1, day='', begin='', end='', type=''):
    creneau = {}
    creneau['id']=id
    creneau['day']=day
    creneau['begin']=begin
    creneau['end']=end
    creneau['type']=type
    app_db.creneaux.insert_one(creneau)

write_creneau(0, 'hors-créneaux', '', '', '1A, 2A, 3A')
write_creneau(1, 'lundi', '11h30', '13h00', '1A, 2A, 3A')
write_creneau(2, 'mardi', '12h30', '14h00', '2A, 3A')
write_creneau(3, 'mardi', '14h15', '15h45', '2A, 3A')
write_creneau(4, 'mardi', '15h00', '16h30', '1A, 2A, 3A')
write_creneau(5, 'mardi', '16h30', '18h00', '1A, 2A, 3A')
write_creneau(6, 'mardi', '18h15', '19h45', '1A, 2A, 3A')
write_creneau(7, 'mercredi', '13h30', '15h00', '1A')
write_creneau(8, 'jeudi', '12h30', '14h00', '2A, 3A')
write_creneau(9, 'jeudi', '14h15', '15h45', '2A, 3A')
write_creneau(10, 'jeudi', '16h00', '17h30', '2A, 3A')
write_creneau(11, 'vendredi', '11h15', '12h45', 'GCC/Archi')


def write_course(id=-1, name='', language='', creneaux =[], min_students=0, max_students=0):
    course={}
    course["id"] = id
    course["name"] = name
    course["language"] = language
    course["creneaux"] = creneaux
    course["min_students"] = min_students
    course["max_students"] = max_students
    app_db.courses.insert_one(course)

write_course(0, "Cours vide", "", [0], 0, 10000)
write_course(1,"Public Speaking", "Anglais", [1], 5, 15)
write_course(2,"Talk Like TED", "Anglais", [1], 5, 15)
write_course(3,"Conversational English", "Anglais", [1], 5, 15)
write_course(4,"Pop Corner", "Anglais", [1], 5, 15)
write_course(5,"Use and Usage (Levels A2-B2 only)", "Anglais", [1], 5, 15)
write_course(6,"Leadership Strategies", "Anglais", [1], 5, 15)
write_course(7,"Art and Engineering", "Anglais", [1], 5, 15)
write_course(8,"Model United Nations", "Anglais", [1], 5, 15)
write_course(9,"Débutants II A1/2", "Allemand", [1,5], 5, 15)
write_course(10,"Mise en situations B1/B2", "Allemand", [1], 5, 15)
write_course(11,"Debatten B2/C1", "Allemand", [1], 5, 15)
write_course(12,"Débutants II", "Espagnol", [1,5], 5, 15)
write_course(13,"Lengua y Creatividad B1", "Espagnol", [1], 5, 15)
write_course(14,"Comunicacion Profesional B2", "Espagnol", [1], 5, 15)
write_course(15,"Interacciones y culturas hispanas B1", "Espagnol", [1], 5, 15)
write_course(16,"Modelo de Naciones Unidas B1-B2", "Espagnol", [1], 5, 15)
write_course(17,"Perfectionner ses écrits académiques et professionels B1/B2", "Français", [1], 5, 15)
write_course(18,"Humours B2-C1", "Français", [1], 5, 15)
write_course(19,"Enigmes et paradoxes de la science B1-C1", "Français", [1], 5, 15)
write_course(20,"Débutants II", "Italien", [1,5], 5, 15)
write_course(21,"Débutants II", "Arabe", [1,5], 5, 15)
write_course(22,"Débutants II", "Chinois", [1,5], 5, 15)
write_course(23,"Débutants II", "Japonais", [1,5], 5, 15)
write_course(24,"Débutants II", "Russe", [1,5], 5, 15)
write_course(25,"Débutants II", "Portugais", [1,5], 5, 15)
write_course(26,"World Issues and Events", "Anglais", [2], 5, 15)
write_course(27,"English Language Games", "Anglais", [2], 5, 15)
write_course(28,"Rock and Roll", "Anglais", [2], 5, 15)
write_course(29,"Unthinkable", "Anglais", [2], 5, 15)
write_course(30,"Civilisations et cultures arabes", "Arabe", [2], 5, 15)
write_course(31,"Telediario B1-B2", "Espagnol", [2], 5, 15)
write_course(32,"Babylon Berlin", "Allemand", [2], 5, 15)
write_course(33,"Débattons de l'actualité B2-C1", "Français", [2], 5, 15)
write_course(34,"Intermédiaires II", "Chinois", [2], 5, 15)
write_course(35,"Photography", "Anglais", [3], 5, 15)
write_course(36,"World Issues and Events", "Anglais", [3], 5, 15)
write_course(37,"Spotlight on Cinema", "Anglais", [3], 5, 15)
write_course(38,"Speak Out", "Anglais", [3], 5, 15)
write_course(39,"Internationales Kulturomosaik", "Allemand", [3], 5, 15)
write_course(40,"Intermédiaires II A2+", "Allemand", [3], 5, 15)
write_course(41,"El arte de hablar en publico B2", "Espagnol", [3], 5, 15)
write_course(42,"Ecos de la planeta en espanol B1-B2", "Espagnol", [3], 5, 15)
write_course(43,"Intermédiaires II", "Arabe", [3], 5, 15)
write_course(44,"Intermédiaires II", "Italien", [3], 5, 15)
write_course(45,"Intermédiaires II", "Russe", [4], 5, 15)
write_course(46,"Culture mosaïque internationale B1-C1", "Français", [3], 5, 15)
write_course(47,"US TV Series", "Anglais", [5], 5, 15)
write_course(48,"American Patchwork", "Anglais", [5], 5, 15)
write_course(49,"Vampire in Our Midst", "Anglais", [5], 5, 15)
write_course(50,"Basic Business Communication (Levels B1-B2 only)", "Anglais", [5], 5, 15)
write_course(51,"Drama Club", "Anglais", [5], 5, 15)
write_course(52,"Modern Dilemmas", "Anglais", [5], 5, 15)
write_course(53,"Keep the Ball Rolling", "Anglais", [5], 5, 15)
write_course(54,"Digital Photography", "Anglais", [5], 5, 15)
write_course(55,"Science et éthique B1-C2", "Français", [5], 5, 15)
write_course(56,"Jeux d'écriture B1-C2", "Français", [5], 5, 15)
write_course(57,"Abenteuergeschichten", "Allemand", [5], 5, 15)
write_course(58,"Escribir y narrar relatos de aventuras B1-B2", "Espagnol", [5], 5, 15)
write_course(59,"Interacciones y culturas hispanas B1", "Espagnol", [5], 5, 15)
write_course(60,"Mexico - retos, cultura e imaginarios", "Espagnol", [5], 5, 15)
write_course(61,"English Debating Club", "Anglais", [6], 5, 15)
write_course(62,"Concerned Photography", "Anglais", [6], 5, 15)
write_course(63,"Debate en espanol B2-C1", "Espagnol", [6], 5, 15)
write_course(64,"Intermédiares II", "Japonais", [6], 5, 15)
write_course(65,"Intermédiares II", "Chinois", [6], 5, 15)
write_course(66,"Intermédiares II", "Italien", [6], 5, 15)
write_course(67,"Dragon's Den", "Anglais", [7], 5, 15)
write_course(68,"Greening Discussions", "Anglais", [7], 5, 15)
write_course(69,"English Project Workshop", "Anglais", [7], 5, 15)
write_course(70,"We Are What We Eat", "Anglais", [7], 5, 15)
write_course(71,"Breaking the News", "Anglais", [7], 5, 15)
write_course(72,"Public Speaking", "Anglais", [7], 5, 15)
write_course(73,"Masterpieces of World Cinema", "Anglais", [7], 5, 15)
write_course(74,"Diskussionen im Spiegel der deutschen Presse B1/B2", "Allemand", [7], 5, 15)
write_course(75,"Atelier mise en scène en espagnol", "Espagnol", [7], 5, 15)
write_course(76,"Language Review (Levels A2-B1 only)", "Anglais", [8], 5, 15)
write_course(77,"Ireland", "Anglais", [8], 5, 15)
write_course(78,"Active English Games", "Anglais", [8], 5, 15)
write_course(79,"Writing Workshop", "Anglais", [8], 5, 15)
write_course(80,"Perfectionner ses écrits professionels B2-C1", "Français", [8], 5, 15)
write_course(81,"English for MS TRADD", "Anglais", [9], 5, 15)
write_course(82,"Communication orale 1 B1.1/B1.2", "Français", [9], 5, 15)
write_course(83,"Communication orale 1 B2.1/C1", "Français", [9], 5, 15)
write_course(84,"Speaking Near and Far", "Anglais", [10], 5, 15)
write_course(85,"Intermédiaires II", "Chinois", [10], 5, 15)
write_course(86,"English for GCC/Archi", "Anglais", [11], 5, 15)
write_course(87,"Book Club", "Anglais", [0], 5, 15)
write_course(88,"Soliya Connect Program", "Anglais", [0], 5, 15)
write_course(89,"Garden Projects", "Anglais", [0], 5, 15)
write_course(90,"Proyecto autonomia guiada", "Espagnol", [0], 5, 15)
write_course(91,"Deutsch mal anders B1", "Allemand", [0], 5, 15)

A = (course(78,"Active English Games", "Anglais", [8], 5, 15)).to_dict()
B = (course(79,"Writing Workshop", "Anglais", [8], 5, 15)).to_dict()
C = (course(80,"Perfectionner ses écrits professionels B2-C1", "Français", [8], 5, 15)).to_dict()
D = (course(81,"English for MS TRADD", "Anglais", [9], 5, 15)).to_dict()
E = (course(82,"Communication orale 1 B1.1/B1.2", "Français", [9], 5, 15)).to_dict()
F = (course(83,"Communication orale 1 B2.1/C1", "Français", [9], 5, 15)).to_dict()
COURSES = [A,B,C,D,E,F]
def write_student(id=-1, name='', vows=[]):
    student={}
    student["id"] = id
    student["name"] = name
    student["vows"] = vows
    student["courses"] = []
    student["type"] = "student"
    student["email"] = ''
    student["token"] = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+ string.digits, k=35))
    app_db.users.insert_one(student)
for i in range(100):
    vow_1 = vow()
    vow_1.courses = [COURSES[(i)%6],COURSES[(i+1)%6],COURSES[(i+2)%6]]
    print(vow_1.courses)
    vow_2 = vow()
    vow_2.courses = [COURSES[(i)%6],COURSES[(i+3)%6]]
    vow_2.weight = 3
    write_student(i, 'st '+ str(i), [vow_1.to_dict(), vow_2.to_dict()])
