from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import PayStubForm,CandidateEntryForm,CandidateSSNForm,IncomeForm,DeductionForm
from .models import Candidate,CandidateSSN,AcceptedCandidate,Employee,Department,Salary,SalaryUnit,Income,Deduction
from django.shortcuts import redirect
from django.utils import timezone

# Create your views here.

def base(request):
	return render(request, 'base.html', {})

def insert_candidate(request):
    if request.method == "POST":
        form = CandidateEntryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('candidate_ssn')
    else:
        form = CandidateEntryForm()
    return render(request, 'newCandidate.html', {'form': form,})

def candidate_ssn(request):
    if request.method == "POST":
        form = CandidateSSNForm(request.POST,request.FILES)
        if form.is_valid():
            canID=Candidate.objects.filter(Name=form.cleaned_data['Name'])
            canID=canID[0]
            candSSN=CandidateSSN(SSN=form.cleaned_data['SSN'],CandidateID=canID)
            candSSN.save()
            return redirect('base')
    else:
        form= CandidateSSNForm()
    return render(request, 'CandidateSSN.html', {'form': form,})

def candidate_list(request):
    candidates = Candidate.objects.all()
    if request.method == "POST":
        body = str(request.body)
        body_unicode=body.split('ID',1)[1] 
        body_unicode= body_unicode.replace("=", "") 
        ID= body_unicode.replace("'", "")
        ID=int(ID)
        if "DELETE" in body:
            Candidate.objects.filter(CandidateID=ID).delete()
        else:
            SSN=CandidateSSN.objects.filter(CandidateID=ID)
            SSN=SSN[0]
            Can=Candidate.objects.filter(CandidateID=ID)
            Can=Can[0]
            A=AcceptedCandidate(SSNID=SSN,CandidateID=Can)
            A.save()
            Candidate.objects.filter(CandidateID=ID).update(IsHired=True)
        return redirect('candidate_list')
    return render(request, 'candidatelist.html', {'candidates': candidates,})

def ACCcandidate_list(request):
    Acandidates = AcceptedCandidate.objects.filter(Assigned=False)
    if request.method == "POST":
        body = str(request.body)
        deptNo=int(body[-4:-1])
        body=body.split('Department',1)[0]
        body=body.split('ID',1)[1]
        body= body.replace("=", "") 
        body= body.replace("'", "")
        body= body.replace("&", "")
        body=body.split('MID',1)
        Can=int(body[0])
        Mid=int(body[1])
        Acandid=AcceptedCandidate.objects.filter(AccCandidateID=Can)[0]
        candid=Acandid.CandidateID
        Dept=Department.objects.filter(DepartmentNo=deptNo)[0]
        if(Mid<=0):
            E=Employee(Name=candid.Name,DepartmentNo=Dept,HiringDate=timezone.now().date(),DateofBirth=candid.DateofBirth,
                Sex=candid.Sex,AccCandidateID=Acandid)
        else:
            Manager=Employee.objects.filter(EmployeeNumber=Mid)[0]
            E=Employee(Name=candid.Name,DepartmentNo=Dept,HiringDate=timezone.now().date(),DateofBirth=candid.DateofBirth,
                Sex=candid.Sex,AccCandidateID=Acandid,ManagerID=Manager)
        E.save()
        AcceptedCandidate.objects.filter(AccCandidateID=Can).update(Assigned=True)
        return redirect('ACCcandidate_list')
        
    return render(request, 'AccCandidatelist.html', {'candidates': Acandidates,})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employeelist.html', {'employees': employees ,})

def PayStub(request):
    form = PayStubForm()
    return render(request, 'newPaystub.html', {'form': form,})

def PayStubView(request):
    if(request.method == 'GET' and 'EmployeeNumber' in str(request.GET)):
        get= str(request.GET)
        body=get.split('EmployeeNumber',1)[1]
        body=body.replace(":", "").replace("'", "").replace(",", "").replace(" ", "") 
        body=body.replace("[", "").replace("]", "").replace("}", "").replace(">", "") 
        body=body.split('Month',1)
        ID=body[0]
        body=body[1]
        body=body.split('Year',1)
        month=body[0]
        year=body[1]
        emp=Employee.objects.filter(EmployeeNumber=ID)[0]
        if Salary.objects.filter(Year=year,Month=month,EmployeeNumber=emp).exists():
            s1=Salary.objects.filter(Year=year,Month=month,EmployeeNumber=emp)[0]
        else:
            s1=Salary(Year=year,Month=month,EmployeeNumber=emp)
            s1.save()
        
    (IncomeT,DeductionT,incomes,deductions,T)=Get_units(s1)
    return render(request, 'Paystub.html', {'s1': s1,'T':T,'IncomeT':IncomeT,'DeductionT':DeductionT,'incomes':incomes,'deductions':deductions,})   

def Add_income(request):
    if request.method=='GET':
        s1= int(request.GET.get('s1'))
        sa=Salary.objects.filter(SalaryId=s1)[0]
        u=SalaryUnit(SalaryId=sa,IsItIncome=True)
        u.save()
        form = IncomeForm()
        return render(request, 'incomeform.html', {'form': form,'s1': s1,'u': u.SalaryUId})
    else:
        return redirect('base')

def Add_deduction(request):
    if request.method=='GET':
        s1= int(request.GET.get('s1'))
        sa=Salary.objects.filter(SalaryId=s1)[0]
        u=SalaryUnit(SalaryId=sa,IsItIncome=False)
        u.save()
        form = DeductionForm()
        return render(request, 'deductionform.html', {'form': form,'s1': s1,'u': u.SalaryUId})
    else:
        return redirect('base')

def Add_income2(request):
    if(request.method == 'GET'):
        s1= int(request.GET.get('s1')) 
        u= int(request.GET.get('u')) 
        amount= int(request.GET.get('amount')) 
        description= request.GET.get('description')
        s1=Salary.objects.filter(SalaryId=s1)[0]
        u=SalaryUnit.objects.filter(SalaryUId=u)[0]
        a=Income(SalaryUId=u,amount=amount,description=description)
        a.save()
        (IncomeT,DeductionT,incomes,deductions,T)=Get_units(s1)
        return render(request, 'Paystub.html', {'s1': s1,'T':T,'IncomeT':IncomeT,'DeductionT':DeductionT,'incomes':incomes,'deductions':deductions,})
    else:
        return redirect('base')



def Add_deduction2(request):
    if(request.method == 'GET'):
        s1= int(request.GET.get('s1')) 
        u= int(request.GET.get('u')) 
        amount= int(request.GET.get('amount')) 
        description= request.GET.get('description')
        s1=Salary.objects.filter(SalaryId=s1)[0]
        u=SalaryUnit.objects.filter(SalaryUId=u)[0]
        a=Deduction(SalaryUId=u,amount=amount,description=description)
        print('here')
        a.save()
        (IncomeT,DeductionT,incomes,deductions,T)=Get_units(s1)
        return render(request, 'Paystub.html', {'s1': s1,'T':T,'IncomeT':IncomeT,'DeductionT':DeductionT,'incomes':incomes,'deductions':deductions,})
    else:
        return redirect('base')

def Get_units(s1):
    units=SalaryUnit.objects.filter(SalaryId=s1)
    incomes=[]
    deductions=[]
    IncomeT=0
    DeductionT=0
    for unit in units:
        if(unit.IsItIncome):
            i=Income.objects.filter(SalaryUId=unit)[0]
            IncomeT=IncomeT+i.amount
            incomes.append(i)
        else:
            i=Deduction.objects.filter(SalaryUId=unit)[0]
            DeductionT=DeductionT+i.amount
            deductions.append(i)
    T=IncomeT-DeductionT
    return (IncomeT,DeductionT,incomes,deductions,T)
