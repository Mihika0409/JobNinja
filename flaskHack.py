from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import getIndeedJobs as indeed
import reviewSorting as rs

import logging

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

app = Flask(__name__)
ask = Ask(app, "/")


@app.route('/')
def homepage():
    return "hi there, how ya doin?"


@ask.launch
def start_skill():
    welcome_message = 'Hello!! Welcome to Job Ninja. I perform job searches based on your skills, and also the good old keyword search. What can I do for you?'
    return question(welcome_message).reprompt("I didnt get you. Give me a skill or keyword.")


# ==============================================================================================================
@ask.intent("YesIntent")
def share_headlines():
    result = "GoodBye"
    return statement(result)


# ==============================================================================================================
@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Cool. All the best for your job search!... byebye'
    return statement(bye_text)


@ask.intent("QueryIntent", mapping={'s1': 'Query'})
def skill_intent(s1):
    session.attributes['skills'] = [s1]
    session.attributes['operation'] = "key"
    return question("Okay, keyword search then! Which city should the jobs be in?").reprompt(
        "I didnt get you. Which city should the jobs be in?")


@ask.intent("SkillIntent", mapping={'s1': 'skill', 's2': 'skillx', 's3': 'skilly'})
def skill_intent(s1, s2, s3):
    skillList = []

    for skill in s1, s2, s3:

        if skill is not None:
            skillList.append(skill)
    session.attributes['skills'] = skillList
    session.attributes['operation'] = 'and'
    return question("Great! Which city should the jobs be in?").reprompt(
        "I didnt get you. Which city should the jobs be in?")


# ==============================================================================================================

@ask.intent("CityIntent", mapping={'city': 'City'})
def getCity(city):
    session.attributes['city'] = city
    ques = "Looking for Jobs in " + city
    return question(ques + ". I can filter results to Full time or intern positions. What would you prefer?").reprompt(
        "Didnt get you. Would you like intern positions or full time?")
    # return question(ques + ". I can give you company reviews based on 1. Overall rating. 2. Work Life balance. 3. Compensation. 4. Job Security. 5. #Management. 6. Culture. 7. CEO Approval. What would you prefer?").reprompt("Didn't get you. Would you like Intern positions or Full time?")


# ==============================================================================================================
@ask.intent("ReviewIntent", mapping={'review': 'Review'})
def getReview(review):
    ind = indeed.indeed()
    session.attributes['review'] = review
    if session.attributes['operation'] == "and":
        res = ind.skill(session.attributes['skills'], session.attributes['city'], session.attributes['jobtype'])
    elif session.attributes['operation'] == "or":
        res = ind.skillOR(session.attributes['skills'], session.attributes['city'], session.attributes['jobtype'])
    else:
        res = ind.skill(session.attributes['skills'], session.attributes['city'], session.attributes['jobtype'])
    if (len(res) == 0):
        return statement(
            "Oops! Looks like our query was too strong for the Internet. I will have to restart, sorry about that!")

	obj = rs.sorts()
	resp = obj.sorting(review, res)
	res = resp
    session.attributes['jobList'] = res[:5]
    statmentList = [(x['jobtitle'], x['company'], x['url']) for x in res]

    urlList = ""
    count = 1
    result = session.attributes['jobtype'] + " Jobs for"
    result = result + " and ".join(session.attributes['skills']) + " in " + session.attributes[
        'city'] + " with preference in " + review + " are "
    for job in statmentList:
        if count < 6:
            result = result + " Job " + str(count) + ": " + job[0].replace("&", "and") + ", at " + job[1].replace("&",
                                                                                                                  "and") + ", "
            urlList = urlList + str(count) + " " + job[0] + ", " + job[1] + " \n URL: " + job[2] + " \n "
            count += 1
            # return statement(result)


    return statement(result + " I've sent this data in a card to your Alexa app. All the best for your job search!..byebye").standard_card(title=session.attributes['jobtype'] + 'Jobs for ' + " , ".join(session.attributes['skills']), text=urlList)


# ==============================================================================================================

@ask.intent("CategoryIntent", mapping={'jobtype': 'Jobtype'})
def getCategory(jobtype):
    session.attributes['jobtype'] = jobtype
    ques = "Looking for " + jobtype + "positions"
    return question(
        ques + ". I can rank the available positions based on 1. Overall rating. 2. Work Life balance. 3. Compensation. 4. Job Security. 5. Management. 6. Culture and 7. CEO Approval. I can also give you jobs based on date posted. What would you prefer?").reprompt(
        "Didn't get you. I can rank the available positions based on 1. Overall rating. 2. Work Life balance. 3. Compensation. 4. Job Security. 5. Management. 6. Culture and 7. CEO Approval. I can also give you jobs based on date posted. What would you prefer?")


# ==============================================================================================================
@ask.intent("SkillIntentOR", mapping={'s1': 'skill', 's2': 'skillx', 's3': 'skilly'})
def skill_intentOR(s1, s2, s3):
    skillList = []

    for skill in s1, s2, s3:
        if skill is not None:
            skillList.append(skill)
    session.attributes['skills'] = skillList
    session.attributes['operation'] = 'or'
    return question("Great! Which city should the jobs be in?").reprompt(
        "I didn't get you. Which city should the jobs be in?")



# #==============================================================================================================
@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Oh! Bye Bye!")


if __name__ == '__main__':
    app.run(debug=True)