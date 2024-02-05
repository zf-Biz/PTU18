"""
Lietuviškai:
Šiame Base.py faile yra aprašytos klasės, kurios duomenų bazės faile sukuria lentelės.
Vartotojas klasėje yra registruojami vartotojų slapyvardžiai, kurie nėra unikalūs. Vartotojas lentelė susijusi su
Testai lentele OneToMany ryšiu.
Testai lentelėje registruojami testą sprendusio vartotojo slapyvardis, testo varianto numeris, testo varianto klausimas,
vartotojo pateiktas atsakymas, iteracijos numeris, kuris parodo, kiek unikalių kartų buvo spręstas testas. Lentelė
Testai susijusi su lentele Vartotojas ManyToOne ryšiu, su lentele Klausimai ManyToOne ryšiu, su lentele Iteracijos
ManyToOne ryšiu.
Iteracijos lentelėje id stulpelis nurodo testo variantą, iteracija stulpelis registruoja, kiek kartu buvo spręstas testo
variantas. Lentelė Iteracijos susijusi su lentele Testai OneToMany ryšiu.
Klausimai lentelėje stulpelyje klausimai yra įrašyti testų klausimai, stulpelyje iteracijos_id nurodytas testo
variantas. Lentelė Klausimai susijusi su lentele testai OneToMany ryšiu, su lentele Atsakymai OneToMany ryšiu, su
lentele Iteracijos ManyToOne ryšiu.
Atsakymai lentelėje atsakymas stulpelyje nurodyti atsakymų variantai į testų klausimus, tiesa_netiesa stulpelyje
nurodyta loginė reikšmė 1 arba 0: 1 reiškia tesitingą atsakymą, 0 - neteisingą, klausimai_id stulpelyje nurodyta, kuriam
klausimui priskirtas atsakymo variantas. Lentelė Atsakymai susijusi su lentele Klausimai ManyToOne ryšiu.

English:
This Base.py file describes the classes that create the tables in the database file.
The Vartotojas (User) class registers user aliases which are not unique. The Vartotojas table refers to
Testai table by the OneToMany relationship.
The Testai (Tests) table records the nickname of the user who took the test, the test
version number, the test version question, the answer given by the user, the iteration number, which indicates the
number of unique number of times the test has been solved. Table Testai is linked to the Vartotojas table ManyToOne
relationship, to the Klausimai table ManyToOne relationship, to the Iteracijos table ManyToOne relationship.
In the Iteracijos (Iterations) table, the id column indicates the variant of the test, the iteracija column records the
number of times the test variant was solved. The Iteracijos table is linked to the Testai table by a OneToMany
relationship.
In the Klausimai (Questions) table, the klausimai column records the test questions, the iteracijos_id column contains
the test  variant id. The Klausimai table is linked to the Testai table by a OneToMany relationship, to the Atsakymai
table by a OneToMany relationship, to the the Iteracijos ManyToOne relationship.
Atsakymai (Answers) table the atsakymai column shows the answer choices for the test
questions, the tiesa_netiesa column indicates the logical value 1 or 0: 1 is a true answer, 0 is a false answer, the
klausimai_id column indicates to which question the answer option assigned. The Atsakymai table is
linked to the Klausimai table by a ManyToOne relationship.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///ORM_finaline_usduotis.db")
Base = declarative_base()

association_table = Table('association', Base.metadata,
                          Column('klausimai_id', Integer, ForeignKey('klausimai.id')),
                          Column('vartotojai_id', Integer, ForeignKey('vartotojai.id')),
                          Column('testai_id', Integer, ForeignKey('testai.id')),
                          Column('iteracijos_id', Integer, ForeignKey('iteracijos.id'))
                          )


class Vartotojai(Base):
    __tablename__ = 'vartotojai'
    id = Column(Integer, primary_key=True)
    vardas = Column(String)
    testai = relationship('Testai', back_populates='vartotojai', cascade='all, delete, delete-orphan')


class Testai(Base):
    __tablename__ = 'testai'
    id = Column(Integer, primary_key=True)
    vartotojai_id = Column(Integer, ForeignKey('vartotojai.id'))
    klausimai_id = Column(Integer, ForeignKey('klausimai.id'))
    taskas = Column(String)
    iteracijos_iteracija = Column(Integer, ForeignKey('iteracijos.iteracija'))
    vartotojai = relationship('Vartotojai', back_populates='testai')
    klausimai = relationship('Klausimai', secondary=association_table, back_populates='testai')
    iteracijos = relationship('Iteracijos', back_populates='testai')


class Iteracijos(Base):
    __tablename__ = 'iteracijos'
    id = Column(Integer, primary_key=True)
    iteracija = Column(Integer)
    testai = relationship('Testai', back_populates='iteracijos', cascade='all, delete, delete-orphan')
    klausimai = relationship('Klausimai', back_populates='iteracija', cascade='all, delete, delete-orphan')


class Klausimai(Base):
    __tablename__ = 'klausimai'
    id = Column(Integer, primary_key=True)
    klausimas = Column(String)
    iteracijos_id = Column(Integer, ForeignKey('iteracijos.id'))
    testai = relationship('Testai', secondary=association_table, back_populates='klausimai')
    atsakymai = relationship('Atsakymai', back_populates='klausimas', cascade='all, delete, delete-orphan')
    iteracija = relationship('Iteracijos', back_populates='klausimai')


class Atsakymai(Base):
    __tablename__ = 'atsakymai'
    id = Column(Integer, primary_key=True)
    atsakymas = Column(String)
    tiesa_netiesa = Column(Integer)
    klausimai_id = Column(Integer, ForeignKey('klausimai.id'))
    klausimas = relationship('Klausimai', back_populates='atsakymai')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


#Žemiau esančios kodo eilutės įrašo į duomenų bazę klausimus su atsakymų variantais.

#Code down below write questions with answers to database.


# iteracija1 = Iteracijos(iteracija=0)
# iteracija2 = Iteracijos(iteracija=0)
# iteracija3 = Iteracijos(iteracija=0)

# session.add(iteracija1)
# session.add(iteracija2)
# session.add((iteracija3))
# session.commit()

# klausimas1 = Klausimai(klausimas='Ar žolė yra žalia?', iteracijos_id=1)
# session.add(klausimas1)
# session.commit()
# klausimas1 = session.query(Klausimai).get(1)
# atsakymas1_1 = Atsakymai(atsakymas='Taip', tiesa_netiesa=1, klausimai_id=1)
# atsakymas1_2 = Atsakymai(atsakymas='Ne', tiesa_netiesa=0, klausimai_id=1)
# klausimas1.atsakymai.extend([atsakymas1_1, atsakymas1_2])
# session.add(klausimas1)
# session.commit()

# klausimas2 = Klausimai(klausimas='Ar dangus yra mėlynas?', iteracijos_id=1)
# session.add(klausimas2)
# session.commit()
# atsakymas2_1 = Atsakymai(atsakymas='Taip', tiesa_netiesa=1, klausimai_id=1)
# atsakymas2_2 = Atsakymai(atsakymas='Ne', tiesa_netiesa=0, klausimai_id=1)
# klausimas2.atsakymai.extend([atsakymas2_1, atsakymas2_2])
# session.add(klausimas2)
# session.commit()

# session.delete(session.query(Klausimai).get(2))
# session.commit()

# klausimas1 = Klausimai(klausimas='Kurį variantą pasirinkus, programa atspausdintų "Hello World" ?', iteracijos_id=2)
# session.add(klausimas1)
# session.commit()
# atsakymas1_1 = Atsakymai(atsakymas='echo("Hello World")', tiesa_netiesa=0, klausimai_id=2)
# atsakymas1_2 = Atsakymai(atsakymas='spausdink("Hello World")', tiesa_netiesa=0, klausimai_id=2)
# atsakymas1_3 = Atsakymai(atsakymas='print("Hello World', tiesa_netiesa=1, klausimai_id=2)
# klausimas1.atsakymai.extend([atsakymas1_1, atsakymas1_2, atsakymas1_3])
# session.add(klausimas1)
# session.commit()
#
# klausimas2 = Klausimai(klausimas='Kuris kintamojo pavadinimas NETEISINGAS ?', iteracijos_id=2)
# session.add(klausimas2)
# session.commit()
# atsakymas2_1 = Atsakymai(atsakymas='my-var', tiesa_netiesa=0, klausimai_id=2)
# atsakymas2_2 = Atsakymai(atsakymas='Myvar', tiesa_netiesa=1, klausimai_id=2)
# atsakymas2_3 = Atsakymai(atsakymas='_myvar', tiesa_netiesa=0, klausimai_id=2)
# klausimas2.atsakymai.extend([atsakymas2_1, atsakymas2_2, atsakymas2_3])
# session.add(klausimas2)
# session.commit()
#
# klausimas3 = Klausimai(klausimas='Kuris variantas sukuria funkciją?', iteracijos_id=2)
# session.add(klausimas3)
# session.commit()
# atsakymas3_1 = Atsakymai(atsakymas='def myFunction():', tiesa_netiesa=1, klausimai_id=2)
# atsakymas3_2 = Atsakymai(atsakymas='create myFunction():', tiesa_netiesa=0, klausimai_id=2)
# atsakymas3_3 = Atsakymai(atsakymas='function myfunction():', tiesa_netiesa=0, klausimai_id=2)
# klausimas3.atsakymai.extend([atsakymas3_1, atsakymas3_2, atsakymas3_3])
# session.add(klausimas3)
# session.commit()
#
# klausimas4 = Klausimai(klausimas='Kuris simbolis žymi daugybos veiksmą ?', iteracijos_id=2)
# session.add(klausimas4)
# session.commit()
# atsakymas4_1 = Atsakymai(atsakymas='+', tiesa_netiesa=0, klausimai_id=2)
# atsakymas4_2 = Atsakymai(atsakymas='*', tiesa_netiesa=1, klausimai_id=2)
# atsakymas4_3 = Atsakymai(atsakymas='%', tiesa_netiesa=0, klausimai_id=2)
# klausimas4.atsakymai.extend([atsakymas4_1, atsakymas4_2, atsakymas4_3])
# session.add(klausimas4)
# session.commit()
#
# klausimas5 = Klausimai(klausimas='Kuris variantas gali būti apibūdintas, kaip TUPLE ?', iteracijos_id=2)
# session.add(klausimas5)
# session.commit()
# atsakymas5_1 = Atsakymai(atsakymas='{"apple","banana","cherry"}', tiesa_netiesa=0, klausimai_id=2)
# atsakymas5_2 = Atsakymai(atsakymas='("apple","banana","cherry")', tiesa_netiesa=1, klausimai_id=2)
# atsakymas5_3 = Atsakymai(atsakymas='["apple","banana","cherry"]', tiesa_netiesa=0, klausimai_id=2)
# klausimas5.atsakymai.extend([atsakymas5_1, atsakymas5_2, atsakymas5_3])
# session.add(klausimas5)
# session.commit()
