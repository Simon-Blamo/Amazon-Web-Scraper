from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time


def getAmazonUsers(url):
    global driver
    driver.get(url) 
    driver.find_element(By.XPATH, '//*[@data-hook="see-all-reviews-link-foot"]').click()
    time.sleep(2)
    for i in range(0, 10):
        count = i+1
        linksToUsersPage = driver.find_elements(By.XPATH, '//div[@class="a-row a-spacing-none"]/div/div/a[@class="a-profile"]')
        textsOfUserName = driver.find_elements(By.XPATH, '//div[@class="a-row a-spacing-none"]/div/div/a[@class="a-profile"]/div[@class="a-profile-content"]/span')
        usersDetails = []
        for j in range(len(linksToUsersPage)):
            userDetail = {}
            userDetail["userPageLink"] = linksToUsersPage[j].get_attribute('href')
            userDetail["userName"] = textsOfUserName[j].text
            usersDetails.append(userDetail)
        pagesOfUsers.append(usersDetails)
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, '//ul[@class="a-pagination"]/li[2]/a').click()
            driver.refresh()
        except:
            break
        print("Review page", count, "grabbed.")
    print("---DONE---")
    
def getReviewValue(s):
    arr = [1, 2, 3, 4, 5]
    for el in arr:
        if str(el) in s:
            return el

def hasEnoughReviews(u):
    global driver
    global totalNumOfUsers
    driver.get(u["userPageLink"])
    time.sleep(4)
    totalNumOfUsers += 1
    return len(driver.find_elements(By.XPATH, '//div[@class="your-content-tab-container"]/div'))

def determineBias(u):
    global driver
    global biasedUsersFound
    scoreArr = [0, 0, 0, 0, 0, 0]
    userReviews = driver.find_elements(By.XPATH, '//div[@class="your-content-tab-container"]/div/a/div/div/div/div/i')
    for i in range(len(userReviews)):
        scoreArr[getReviewValue(userReviews[i].get_attribute('class'))] += 1
    
    total = sum(scoreArr)
    percentageHelper = 100/total
    with open('biasedUsersResults.txt', 'a') as file:
        if(scoreArr[5] * percentageHelper) >= 80 or (scoreArr[1] * percentageHelper) >= 80:
            if (scoreArr[5] * percentageHelper) >= 80 :
                file.write("(*) " + u["userName"] + " " + u["userPageLink"] + "\n"+ u["userName"] + " is a biased user due to too many 5-star reviews\n\n")
            else:
                file.write("(*) " +  u["userName"] + " " + u["userPageLink"] + "\n" + u["userName"] + " is a biased user due to too many 1-star reviews\n\n")
            biasedUsersFound += 1
        else:
            file.write("(!) " + u["userName"] + " " + u["userPageLink"] + "\n" + u["userName"] + " is NOT a biased user.\n\n")
    

pagesOfUsers = []
biasedUsersFound = 0
totalNumOfUsers = 0
open("biasedUsersResults.txt", "w")
userSelect = int(input("Enter 1 to get the reviews of the default of product given.\nEnter 2 to enter a link to a different product.\nOption: "))
if userSelect != 1 and userSelect != 2:
    while True:
        userSelect = int(input("Enter valid option:"))
        if userSelect != 1 or userSelect != 2:
            break
if userSelect == 1:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = 'https://a.co/d/hahQlID'
    getAmazonUsers(url)
elif userSelect == 2:
    url = input("Enter your custom URL:")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    getAmazonUsers(url)

with open('users.json','w') as fp:
    if pagesOfUsers:
        for page in pagesOfUsers:
            print("Dumping all users found in the users.json!")
            json.dump(page, fp)
            fp.write("\n")

for page in pagesOfUsers:
    for dict in page:
        if hasEnoughReviews(dict) >= 15:
            print("Determining if", dict["userName"], "is biased...\n")
            determineBias(dict)
        
print("\n\nTotal number of users:", totalNumOfUsers)
print("Total number of biased users found: " + str(biasedUsersFound) + "(" + str(round((100/totalNumOfUsers) * biasedUsersFound, 2)) + "%)")
driver.quit()