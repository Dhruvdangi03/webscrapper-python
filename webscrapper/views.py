from django.shortcuts import render
from .forms import ExtractionForm
from .models import ExtractedData
from selenium import webdriver

# Create your views here.
def extract_data(url,xpath):
    driver = webdriver.Chrome()
    driver.get(url)
    element = driver.find_element("xpath",xpath)
    data = element.text
    driver.quit()
    return data

def all_Details(request):
    app = ExtractedData.objects.all()
    return render(request, 'bot/app.html',{'app':app})

def savedata(request):
    if request.method=="POST":
        site = request.POST.get('site')
        xpath = request.POST.get('xpath')
        data = request.POST.get('data')
        creation_time = request.POST.get('creation_time')
        en = ExtractedData(site=site,xpath=xpath,data=data,creation_time=creation_time)
        en.save()
    print(en)
    return render(request, 'bot/form.html')

def extract(request):
    if request.method == 'POST':
        form = ExtractionForm(request.POST)
        if form.is_valid():
            site = form.cleaned_data['site']
            xpath = form.cleaned_data['xpath']
            data = extract_data(site, xpath)
            extracted_data = ExtractedData(site=site, xpath=xpath, data=data)
            extracted_data.save()
            return render(request, 'bot/app.html', {'data': data})
    else:
        form = ExtractionForm()
    return render(request, 'bot/form.html', {'form': form})
