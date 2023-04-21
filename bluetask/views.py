from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import System, SystemContract
from .forms import SystemContractForm   

def index(request):
    data = SystemContract.objects.all().values()
    data2 = System.objects.all().values()
    form = SystemContractForm()
    if request.method == 'POST':
        file = request.FILES.get('file')
        # Checking if file is Excel file and if it has been uploaded
        if not file.name.endswith('.xls') and not file.name.endswith('.xlsx'):
            return JsonResponse({'status': 'error', 'message': 'File is not Excel file'})
        # Handling data validation and saving to database
        try:
            # Reading data from Excel file
            # Forcing some columns to be read as string in order to avoid issues with empty rows
            data = pd.read_excel(file, dtype={
                'amount_period': 'object',
                'amount_type': 'object',
                'order_number': 'object',
                'request': 'object'
            })
            # Checking if columns match the model
            fields = [field.name for field in SystemContract._meta.fields]
            fields.remove('id')
            if set(data.columns) == set(fields):
                pass
            else:
                return JsonResponse({'status': 'error', 'message': 'Columns don\'t match, please check the Excel file'})
            data = data.to_dict('records')
            errors=[]
            # Iterating through the rows and saving to database
            for idx, row in enumerate(data):
                # Checking if system exists in the database
                try:
                    system = System.objects.get(name=row['system'])
                except System.DoesNotExist:
                    errors.append( {'message': "System from this row doesn't exist in the database", 'row_number': idx + 2})
                    continue
                model = SystemContract(system=system, request=str(row['request']), order_number=row['order_number'], from_date=row['from_date'], to_date=row['to_date'], amount=str(row['amount']), amount_type=row['amount_type'], amount_period=row['amount_period'], authorization_percent=str(row['authorization_percent']), active=row['active'])
                # Data validation
                try:
                    model.full_clean()
                    model.save()
                except Exception as e:
                    errors.append({'message': repr(e), 'row_number': idx + 2})
            if errors:
                message = 'The following errors occurred:\n'
                for error in errors:
                    message += "Row " + str(error['row_number']) + " : " + error['message'] + "\n"
                return JsonResponse({'status': 'error', 'message': message})
            else:
                return JsonResponse({'status': 'success', 'message': 'Import successful'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    context = {'data':list(data), 'data2':list(data2), 'form':form}
    return render(request, 'index.html', context)        
  

def delete_record(request):
    if request.method == 'POST':
        system_contracts_id = request.POST.get('system_contracts_id')
        try:
            # loading record by id
            system_contracts = SystemContract.objects.get(id=system_contracts_id)
            # deleting record
            system_contracts.delete()
            # sending response
            return JsonResponse({'status': 'success', 'message': 'Record deleted'})
        except SystemContract.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Record doesn\'t exist'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Wrong request'})

# adding new record or updating existing record    
def add_record(request):
    if request.method == 'POST':
        form = SystemContractForm(request.POST)
        id_in_form = request.POST.get('id_in_form')
        # Checking if form is valid
        if form.is_valid():
            # Checcking if record is new or existing
            try: 
                system_contract = SystemContract.objects.get(id=id_in_form)
            except:
                system_contract = None
            # If record is old, updating it    
            if system_contract is not None:
                system = System.objects.get(id=form.data['system'])
                system_contract.system = system
                system_contract.request = form.data['request']
                system_contract.order_number = form.data['order_number']
                system_contract.from_date = form.data['from_date']
                system_contract.to_date = form.data['to_date']
                system_contract.amount = form.data['amount']
                system_contract.amount_type = form.data['amount_type']
                system_contract.amount_period = form.data['amount_period']
                system_contract.authorization_percent = form.data['authorization_percent']
                if form.data.get('active') == 'on':
                    system_contract.active = 'True'  
                else:
                    system_contract.active = 'False'
                try:
                    system_contract.full_clean()
                    system_contract.save()
                    return JsonResponse({'status': 'success', 'message': 'Record updated'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': repr(e)})
            # If record is new, adding it
            else:
                try:
                    form.save()
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': repr(e)})
            return JsonResponse({'status': 'success', 'message': 'Record updated or added'})
        else:
            # When form is not valid checking if record already exists and user does not change system or request and updating it.
            if 'System contract with this Request and System already exists.' in form.errors.values().__str__():
                system_contract = SystemContract.objects.get(request=form.data['request'], system=form.data['system'])
                system_contract.order_number = form.data['order_number']
                system_contract.from_date = form.data['from_date']
                system_contract.to_date = form.data['to_date']
                system_contract.amount = form.data['amount']
                system_contract.amount_type = form.data['amount_type']
                system_contract.amount_period = form.data['amount_period']
                system_contract.authorization_percent = form.data['authorization_percent']
                if form.data.get('active') == 'on':
                    system_contract.active = 'True'  
                else:
                    system_contract.active = 'False'
                try:
                    system_contract.full_clean()
                    system_contract.save()
                    return JsonResponse({'status': 'success', 'message': 'Record updated or added'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': repr(e)}) 
            else:
                return JsonResponse({'status': 'error', 'message': 'Wrong request'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Wrong request'})

# loading data to table    
def reload_table(request):
    if request.method == 'GET':
        data = SystemContract.objects.all().values()
        return JsonResponse({'status': 'success', 'data':list(data)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Wrong request'}) 
