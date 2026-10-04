import joblib, numpy as np
from sklearn.metrics import accuracy_score, classification_report

model      = joblib.load('models/department_model.pkl')
vectorizer = joblib.load('models/dept_vectorizer.pkl')
le         = joblib.load('models/dept_label_encoder.pkl')

# 120 completely UNSEEN samples — 10 per department (not in training data)
test_data = [
    # ---- HR (10) ----
    ('HR', 'I need to check my remaining casual leave balance'),
    ('HR', 'Please help me update my home address in company records'),
    ('HR', 'How many sick leaves am I entitled to per year'),
    ('HR', 'I want to raise a formal complaint against my manager'),
    ('HR', 'Can I get my appointment letter reissued with current CTC'),
    ('HR', 'I need a salary advance this month for personal emergency'),
    ('HR', 'My PF account is not linked to my Aadhar card'),
    ('HR', 'What is the company dress code and grooming policy'),
    ('HR', 'I need my payslip for bank home loan application'),
    ('HR', 'What documents are needed for background verification process'),

    # ---- IT Support (10) ----
    ('IT Support', 'My desktop computer will not start at all please help'),
    ('IT Support', 'I need help recovering deleted emails from Outlook inbox'),
    ('IT Support', 'The software update is stuck at 80 percent for hours'),
    ('IT Support', 'I need a new wireless mouse and keyboard for my workstation'),
    ('IT Support', 'My Teams presence status is always showing offline'),
    ('IT Support', 'The company employee portal login page is not loading'),
    ('IT Support', 'I need help connecting to the network printer remotely'),
    ('IT Support', 'My hard disk is making a clicking noise and data is at risk'),
    ('IT Support', 'I cannot open any PDF files on my computer'),
    ('IT Support', 'My laptop overheats within 10 minutes and shuts down'),

    # ---- Accounts (10) ----
    ('Accounts', 'Please share the monthly expense summary report for September'),
    ('Accounts', 'I need to know the outstanding dues for a key vendor'),
    ('Accounts', 'Salary for the contract employees has not been processed yet'),
    ('Accounts', 'I need a certified copy of our company financial statements'),
    ('Accounts', 'Please release the advance payment for the ongoing project'),
    ('Accounts', 'I need to submit my tax saving investment proof this month'),
    ('Accounts', 'Our client has raised a dispute about the invoiced amount'),
    ('Accounts', 'I need to initiate a wire transfer for the overseas supplier'),
    ('Accounts', 'Please provide journal entries for the last quarter'),
    ('Accounts', 'I need to know the remaining budget for my department'),

    # ---- Security (10) ----
    ('Security', 'I need a temporary gate pass issued for my external contractor'),
    ('Security', 'Please extend my after-hours office access for night shift'),
    ('Security', 'I noticed a broken lock on the emergency exit door today'),
    ('Security', 'A visitor is creating disturbance at the reception area'),
    ('Security', 'I need to report suspicious phone calls received at the office'),
    ('Security', 'Please check the camera footage near the parking entrance'),
    ('Security', 'Someone stole my bag from the cafeteria earlier today'),
    ('Security', 'I need a security escort from the main gate to my cabin'),
    ('Security', 'The access control reader at gate 2 is showing an error'),
    ('Security', 'I need a clearance letter to carry server equipment outside office'),

    # ---- Administration (10) ----
    ('Administration', 'Please arrange a projector and screen for team training tomorrow'),
    ('Administration', 'I need to relocate my entire team to a different floor'),
    ('Administration', 'Please help book a flight ticket for urgent business travel'),
    ('Administration', 'The office coffee machine needs to be cleaned and serviced'),
    ('Administration', 'I need to print and bind 50 copies of the annual report'),
    ('Administration', 'Please arrange a van to transport office equipment to the venue'),
    ('Administration', 'I need name plates printed for newly joined team members'),
    ('Administration', 'Please stock up on A4 paper and printer toner cartridges'),
    ('Administration', 'I need help planning and organizing a team outing for 20 people'),
    ('Administration', 'Please arrange canteen lunch boxes for the outstation staff'),

    # ---- Network (10) ----
    ('Network', 'I need help diagnosing packet loss on my network connection'),
    ('Network', 'The office internet goes down every evening around 6 PM'),
    ('Network', 'Please check why the VPN tunnel keeps dropping so frequently'),
    ('Network', 'I need a dedicated static IP address for my development server'),
    ('Network', 'The network printer cannot be discovered on the local area network'),
    ('Network', 'Please extend the WiFi coverage to the rooftop terrace area'),
    ('Network', 'The DNS server is returning wrong or incorrect IP addresses'),
    ('Network', 'I need to open a specific firewall port for our cloud application'),
    ('Network', 'The WAN link between our two branch offices has been unstable'),
    ('Network', 'I need a network topology map drawn for the new office floor'),

    # ---- Facilities & Maintenance (10) ----
    ('Facilities & Maintenance', 'The air conditioning unit in my cabin is not cooling properly'),
    ('Facilities & Maintenance', 'I need a plumber to fix the blocked drain in the restroom'),
    ('Facilities & Maintenance', 'The overhead light in the corridor near my desk is flickering'),
    ('Facilities & Maintenance', 'The office building elevator is making grinding noises'),
    ('Facilities & Maintenance', 'I need an electrician to fix the power socket at my workstation'),
    ('Facilities & Maintenance', 'The water dispenser on the first floor is leaking continuously'),
    ('Facilities & Maintenance', 'Please arrange a carpenter to repair the broken storage cabinet'),
    ('Facilities & Maintenance', 'The office generator diesel tank needs to be refilled urgently'),
    ('Facilities & Maintenance', 'I need to report a pest infestation near the pantry area'),
    ('Facilities & Maintenance', 'The washroom flush is not working on the second floor'),

    # ---- Quality Assurance (10) ----
    ('Quality Assurance', 'I need a QA review completed before we push to production'),
    ('Quality Assurance', 'The latest build has multiple test failures that need investigation'),
    ('Quality Assurance', 'Please provide a defect summary report for the last two weeks'),
    ('Quality Assurance', 'I need the product batch certified as per ISO 9001 standards'),
    ('Quality Assurance', 'The manual testing of the new payment module is not complete'),
    ('Quality Assurance', 'I need a test strategy document prepared for the upcoming release'),
    ('Quality Assurance', 'A critical bug was found in production and needs root cause analysis'),
    ('Quality Assurance', 'The test coverage for the new API endpoints is insufficient'),
    ('Quality Assurance', 'I need QA approval before deploying the patch to live environment'),
    ('Quality Assurance', 'The raw material incoming inspection report is pending sign off'),

    # ---- Data / Analytics (10) ----
    ('Data / Analytics', 'I need a weekly sales performance dashboard built in Power BI'),
    ('Data / Analytics', 'Please extract last quarter revenue data from the CRM database'),
    ('Data / Analytics', 'The automated report sent to management has wrong numbers'),
    ('Data / Analytics', 'I need a customer churn prediction model built for the sales team'),
    ('Data / Analytics', 'Please create a Tableau visualization for the marketing campaign'),
    ('Data / Analytics', 'The data ingestion pipeline broke and records are missing'),
    ('Data / Analytics', 'I need help writing an optimized SQL query for my finance report'),
    ('Data / Analytics', 'Please analyze the user drop-off at each step of our signup funnel'),
    ('Data / Analytics', 'The machine learning model output has significantly drifted recently'),
    ('Data / Analytics', 'I need a dataset cleaned and ready for the analytics team'),

    # ---- Engineering (10) ----
    ('Engineering', 'I need a mechanical drawing reviewed for the new bracket design'),
    ('Engineering', 'The production machine line is throwing a fault code and has stopped'),
    ('Engineering', 'Please help me debug the embedded firmware for the new board'),
    ('Engineering', 'The 3D CAD model of the housing needs to be corrected'),
    ('Engineering', 'I need a complete bill of materials for the hardware prototype'),
    ('Engineering', 'The hydraulic system is showing excessive pressure fluctuations'),
    ('Engineering', 'I need an engineering change request raised for the latest revision'),
    ('Engineering', 'The servo drive calibration is off and needs to be corrected'),
    ('Engineering', 'I need EMC compliance testing arranged for the new product'),
    ('Engineering', 'The welded joint on the structure failed the non-destructive test'),

    # ---- Product Development (10) ----
    ('Product Development', 'I need the product roadmap updated for the next two quarters'),
    ('Product Development', 'The feature requirements spec is incomplete and needs a review'),
    ('Product Development', 'I need user stories written for the new mobile checkout experience'),
    ('Product Development', 'Please schedule a product backlog refinement session this week'),
    ('Product Development', 'I need a competitive analysis done for the new feature we are planning'),
    ('Product Development', 'The product demo for the board needs to be prepared by Friday'),
    ('Product Development', 'I need to define the success metrics before we begin development'),
    ('Product Development', 'The beta users gave negative feedback on the new onboarding flow'),
    ('Product Development', 'I need to create a go-to-market plan for the new product launch'),
    ('Product Development', 'The product north star metric has not been defined for this quarter'),

    # ---- Research & Development (10) ----
    ('Research & Development', 'I need access to IEEE papers for my ongoing research project'),
    ('Research & Development', 'Please procure specific reagents for the laboratory experiment'),
    ('Research & Development', 'The spectrometer in the lab needs urgent recalibration'),
    ('Research & Development', 'I need help drafting the introduction section of the research paper'),
    ('Research & Development', 'We discovered a novel compound and need to start the patent process'),
    ('Research & Development', 'The lab experiment results are inconsistent across repeated trials'),
    ('Research & Development', 'I need funding request approved for the new research initiative'),
    ('Research & Development', 'Please schedule a progress review with the research principal'),
    ('Research & Development', 'I need to present findings from our latest study at a conference'),
    ('Research & Development', 'The lab safety equipment needs inspection before we resume trials'),
]

test_texts  = [t for _, t in test_data]
test_labels = [d for d, _ in test_data]

X_test  = vectorizer.transform(test_texts)
y_test  = le.transform(test_labels)
y_pred  = model.predict(X_test)
y_proba = model.predict_proba(X_test)

total   = len(test_texts)
correct = int(accuracy_score(y_test, y_pred, normalize=False))
wrong   = total - correct
acc     = correct / total * 100

print()
print('='*65)
print('  OVERALL MODEL ACCURACY ON %d UNSEEN SAMPLES' % total)
print('='*65)
print()
print('  Total Samples      : %d' % total)
print('  Correctly Routed   : %d' % correct)
print('  Incorrectly Routed : %d' % wrong)
print()
print('  OVERALL ACCURACY   : %d / %d  (%.1f%%)' % (correct, total, acc))
print()
print('='*65)
print('  PER-DEPARTMENT BREAKDOWN')
print('='*65)
print('  %-28s  Correct  Total  %%     Confidence' % 'Department')
print('  ' + '-'*60)

dept_results = {}
for i, dept in enumerate(test_labels):
    predicted = le.classes_[y_pred[i]]
    conf = float(max(y_proba[i]))
    hit = (predicted == dept)
    if dept not in dept_results:
        dept_results[dept] = {'correct': 0, 'total': 0, 'confs': []}
    dept_results[dept]['total'] += 1
    dept_results[dept]['confs'].append(conf)
    if hit:
        dept_results[dept]['correct'] += 1

for dept in le.classes_:
    if dept in dept_results:
        r   = dept_results[dept]
        c   = r['correct']
        t   = r['total']
        pct = c / t * 100
        avg_conf = sum(r['confs']) / len(r['confs'])
        bar = '#' * c + '-' * (t - c)
        grade = 'EXCELLENT' if pct >= 90 else 'GOOD' if pct >= 70 else 'FAIR' if pct >= 50 else 'LOW'
        print('  %-28s    %2d      %2d    %3.0f%%   avg_conf=%.2f  [%s]  %s' % (
            dept, c, t, pct, avg_conf, bar, grade))

print()
print('='*65)
print('  FINAL SCORE : %d / %d   ACCURACY : %.1f%%' % (correct, total, acc))
if acc >= 80:
    verdict = 'EXCELLENT'
elif acc >= 65:
    verdict = 'GOOD'
elif acc >= 50:
    verdict = 'FAIR'
else:
    verdict = 'NEEDS MORE DATA'
print('  VERDICT     : %s' % verdict)
print('  NOTE: Emails with confidence < 0.45 go to manual_review')
print('='*65)
