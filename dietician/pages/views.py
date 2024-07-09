from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import os
import google.generativeai as genai
from PIL import Image
import re
import datetime

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create your views here.
def cal(text):
# Extract total calories
    total_calories_match = re.search(r"Total Calories: (\d+) calories", text)
    if total_calories_match:
        total_calories = int(total_calories_match.group(1))
    else:
        total_calories = None

    # Extract percentages using a loop (assuming consistent format)
    percentages = {}
    for line in text.splitlines():
        match = re.search(r"(\w+): (\d+)g", line)
        if match:
            nutrient, value = match.groups()
            percentages[nutrient] = int(value)
    
    lines = text.splitlines()

    # Extract names by splitting each line at the hyphen and taking the first element
    names = [line.split(" - ")[0] for line in lines if "-" in line]
    data = {
        "date_time": datetime.datetime.now(),
        "total_calories": total_calories,
        "percentages": percentages,
        "names": names
    }
    return data

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-1.5-pro-latest')
    response=model.generate_content([input,image,prompt])
    return response.text

@csrf_exempt
def nutriscan(request):
    response=''
    img=''
    if request.method=='POST':
        data=request.POST
        inputPrompt=data['inputPrompt']
        inputImage=request.FILES.get('inputImage')
        img=inputImage
        if inputImage is not None:
            inputImage = Image.open(inputImage)
        print(inputImage)
        print(inputPrompt)
        
        prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               strictly in below format
            
               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
               Total Calories: xxx calories
Finally you must also mention whether the items are healthy or not.
Must also mention grams of carbohydatres, proteins, fats, fibers, sugars, 
and other things which you can observe in the food items strictly in below format
                Carbohydrates: xxg
                Proteins: xxg
                Fats: xxg
                Fibers: xxg
                Sugars: xxg
                Others: xxg
Give detailed information about the food items and its health impact.

"""
        response=get_gemini_repsonse(prompt,inputImage,inputPrompt)
        print(response)
        return JsonResponse({'message':response})
    
    return render(request,'nutriscan.html')

@csrf_exempt
def pack(request):
    if request.method=='POST':
        data=request.POST
        inputPrompt=data['inputPrompt']
        inputImage=request.FILES.get('inputImage')
        if inputImage is not None:
            inputImage = Image.open(inputImage)
        print(inputImage)
        print(inputPrompt)

        prompt="""
You are an expert nutritionist and doctor where you need to see the ingredients of a packaged food or medicine or any other edible packaged items from the image
and output the harmful contents, beneficial contents, overall impact and additional information based on the user's health conditions.
The user will provide the health conditions and the image of the ingredients list of the food item.
Output:

Harmful Contents: List any ingredients in the food that could be harmful based on your health conditions. Explain the potential negative effects of these ingredients.
Beneficial Contents: Highlight any ingredients that could be beneficial for your health.

Overall Impact: Provide a clear recommendation on whether the food item is healthy, unhealthy, risky, or neutral for you to consume, considering your health conditions.

Additional Information: Offer suggestions for alternative food items that might be more suitable for your needs.

Nutrient Breakdown: Calculate and display the amount of key nutrients (calories, sugar, fat, protein) in the food item.

Give this food item a rating out of 100 based on its healthiness. Also add unit of healthiness.

Remember to change lines between each subpart of the output.
"""

        response=get_gemini_repsonse(prompt,inputImage,inputPrompt)
        print(response)
        return JsonResponse({'message':response})
    
    return render(request,'packaged.html')

def home(request):
    return render(request,'home.html')