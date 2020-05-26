from experta import *
import sys

class Personne(Fact):
    """Info about the patient"""
    pass


def SUMFIELDS(p, *fields):
    return sum([p.get(x, 0) for x in fields])


class InreferenceEngine(KnowledgeEngine):
    @Rule(Personne(since_when_uneasiness=P(lambda x: x <= 14)))
    def concerned_person(self):
        #print("aaaao")
        self.declare(Fact(concerned=True))
	
    
    
    @Rule(Fact(concerned=True),
           Personne(cough=False),
          Personne(muscle_pain=True),
          Personne(nausea_vomiting=True),
          Personne(diff_breathing=False),
          Personne(chest_tightness=False),
          Personne(Fever=True),
          Personne(fam_diabetes=False),
          Personne(fam_hypertension=False),
          Personne(fam_lung_disease=False),
          Personne(fam_heart_disease=False),
          Personne(int_travel_last_14=False),
          Personne(health_care_worker=False),
          Personne(interacted_with_covid=False),
          Personne(police_control=False))
    def malaria(self):
        print("You probably have malaria as you don't have any coughing or difficulty in breathing, major covid symptoms, should take rest")
        print("Artemisinin-based combination therapies (ACTs). ACTs are, in many cases, the first line treatment for malaria.")
        self.declare(Fact(malaria=True))
		
		
    @Rule(Fact(concerned=True),
           Personne(cough=True),
          Personne(muscle_pain=True),
          Personne(nausea_vomiting=False),
          Personne(diff_breathing=False),
          Personne(Fever=False),
          Personne(chest_tightness=True),
          Personne(fam_diabetes=False),
          Personne(fam_hypertension=False),
          Personne(fam_lung_disease=False),
          Personne(fam_heart_disease=False),
          Personne(int_travel_last_14=False),
          Personne(health_care_worker=False),
          Personne(interacted_with_covid=False),
          Personne(police_control=False))
    def bronchitis(self):
        print("You probably have bronchitus or other related respiratory disease, no need to worry no major covid symptoms, should take rest")
        print("Taking over-the-counter medications such as aspirin, acetaminophen, or ibuprofen can help relieve symptoms of bronchitis")
        self.declare(Fact(bronchitis=True))
		
		
    @Rule(Fact(concerned=True),
          AS.p << Personne(),
          TEST(lambda p: SUMFIELDS(p,
                                   'cough',
                                   'diff_breathing',
                                   'Fever') > 1))
    def may_be_COVID_positive(self, p):
        #print("cooorrrona")
        self.declare(Fact(may_be_COVID_positive=True))
		
	
    @Rule(Fact(concerned=True),
          AS.p << Personne(),
          TEST(lambda p: SUMFIELDS(p,
                                   'fam_diabetes',
                                   'fam_diabetes',
                                   'fam_hypertension',
								   'fam_lung_disease') <2))
    def mild_family_risk(self, p):
        #print("hereee")
        self.declare(Fact(mild_family_risk=True))
		
		
    @Rule(Fact(concerned=True),
          AS.p << Personne(),
          TEST(lambda p: SUMFIELDS(p,
                                   'fam_diabetes',
                                   'fam_diabetes',
                                   'fam_hypertension',
								   'fam_lung_disease') > 1))
    def severe_family_risk(self, p):
        #print("familyyy")
        self.declare(Fact(severe_family_risk=True))
		
    @Rule(Fact(concerned=True),
          AS.p << Personne(),
          TEST(lambda p: SUMFIELDS(p,
                                   'int_travel_last_14',
                                   'interacted_with_covid',
                                   'health_care_worker',
								   'police_control') > 0))
    def severe_interactions(self, p):
        #print("travelll")
        self.declare(Fact(severe_interactions=True))

    @Rule(Fact(concerned=True),
          AS.p << Personne(),
          TEST(lambda p: SUMFIELDS(p,
                                   'int_travel_last_14',
                                   'interacted_with_covid',
                                   'health_care_worker',
								   'police_control') < 1 ))
    def mild_interactions(self, p):
        #print("less")
        self.declare(Fact(mild_interactions=True))
		
    @Rule(Fact(concerned=True),
          Fact(may_be_COVID_positive=True),
		  Fact(mild_family_risk=True))
    def self_isolate(self):
        self.declare(Fact(self_isolate=True))
		
    @Rule(Fact(concerned=True),
          Fact(may_be_COVID_positive=True),
		  Fact(severe_family_risk=True))
    def self_quarantine(self):
        #print("self")
        self.declare(Fact(self_quarantine=True))

    @Rule(Fact(concerned=True),
		  Fact(self_quarantine=True),
		  Fact(severe_interactions=True))
    def consult_doctor_immediately1(self):
        print("ALERT!!! ...very high chances of corona as you have symptoms, some family history too, and interactions also  \n");
        print("Kindly get yourself checked as you have the disease probably")
        self.declare(Fact(consolt_doctor_immediately1=True))
		
		
    @Rule(Fact(concerned=True),
		  Fact(self_quarantine=True),
		  Fact(mild_interactions=True))
    def consult_doctor_immediately(self):
        print("Very high chances of corona, as you have symptoms and family hostory, since not traveled anywhere, no interactions, might be community spread  \n");
        print("You are adviced to avoid close contact with anyone, and consult the doctor as soon as possible")
        self.declare(Fact(consolt_doctor_immediately=True))
		
		
		
    @Rule(Fact(concerned=True),
		  Fact(self_isolate=True),
		  Fact(severe_interactions=True))
    def consult_doctor(self):
        print("high chances of corona, no family history but symptoms with travel history or interactions, consult doctor");
        print("You are adviced to avoid close contact with anyone and also isolate yourself,don't delay any further, and consult the doctor as soon as possible")
        self.declare(Fact(consolt_doctor=True))
		
    
    @Rule(Fact(concerned=True),
		  Fact(self_isolate=True),
		  Fact(mild_interactions=True))
    def consult_doctor1(self):
        print("Chances of corona, no family or travel history but symptoms so safe to get a checkup. \n")
        print("Suggest you to not interact with anyone")
        self.declare(Fact(consolt_doctor1=True))
		
		
engine = InreferenceEngine()
engine.reset()
print("I will ask you a few questions, please reply in True or False")
val1=input("Since when are you feeling uneasy: ")


val2=input("Do you have coughing: ")
if val2=="Yes":	
    val2=True
else:
    val2=False

val3=input("Do you have muscle pain: ")
if val3=="Yes":	
    val3=True
else:
    val3=False
	
val15=input("Are you experiencing chest tightness: ")
if val15=="Yes":	
    val15=True
else:
    val15=False
	
	
val4=input("Are you experiencing nausea_vomiting: ")
if val4=="Yes":	
    val4=True
else:
    val4=False
	
	
val5=input("Are you having difficulty in breathing: ")
if val5=="Yes":	
    val5=True
else:
    val5=False
	
	
val6=input("Are you having some fever: ")
if val6=="Yes":	
    val6=True
else:
    val6=False
	
val7=input("Does anyone have diabetes in your family: ")
if val7=="Yes":
    val7=True
else:
    val7=False
	
val8=input("Does anyone have hypertension in your family: ")
if val8=="Yes":
    val8=True
else:
    val8=False
	
val9=input("Does anyone have any lung disease in your family: ")
if val9=="Yes":
    val9=True
else:
    val9=False
	
val10=input("Does anyone have any heart disease in your family: ")
if val10=="Yes":
    val10=True
else:
    val10=False
	
val11=input("Have you travelled internationally in last 14 days: ")
if val11=="Yes":
    val11=True
    #print("tr")
else:
    val11=False
	
val12=input("Have you interacted woth a covid patient recently: ")
if val12=="Yes":
    val12=True
    #print("tr")
else:
    val12=False
	
	
val13=input("Are you a health care worker: ")
if val13=="Yes":
    val13=True
    #print("tr")
else:
    val13=False
	
	
val14=input("Are you in police control service: ")
if val14=="Yes":
    val14=True
    #print("tr")
else:
    val14=False
	
	
engine.declare(Personne(since_when_uneasiness=int(val1),
                        cough=val2,
                        muscle_pain=val3,
                        nausea_vomiting=val4,
                        chest_tightness=val15,
                        diff_breathing=val5,
                        Fever=val6,
                        fam_diabetes=val7,
                        fam_hypertension=val8,
                        fam_lung_disease=val9,
                        fam_heart_disease=val10,
                        int_travel_last_14=val11,
                        health_care_worker=val12,
                        interacted_with_covid=val13,
                        police_control=val14							
                        ))

engine.run()