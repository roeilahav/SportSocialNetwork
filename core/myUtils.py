
import math 
import ast 


def string_to_list(string):
    result = ast.literal_eval(string)
    return result

#euclideanFormula applied on two 2d list of preferences 
def euclideanFormula(myPreferences , prefereces):
        sum = 0 
        for i in range(len(myPreferences)):
            sum += (myPreferences[i][1] - prefereces[i][1])**2
        sqrtAns = math.sqrt(sum) 
        return sqrtAns
    
def sortMatrix(matrix):
    matrix.sort(key = lambda x: x[1] , reverse = False)
    return matrix


def getListOfProfiles(matrix):
    listOfProfiles = []
    for i in range(len(matrix)):
        listOfProfiles.append(matrix[i][0])
    return listOfProfiles


def getMatchingProfiles(allProfles , myProfile):
   
    prefereces = []
    for profile in allProfles: 
        print(profile , profile.getPreferences())
        simPref = profile.getPreferences()
        simPref = string_to_list(simPref) 

        prefereces.append(simPref)
    print("PREFERE" , prefereces)

    #convert my pref string to list 
    myPreferences = myProfile.getPreferences()
    print("MY PREF" , myPreferences)
    #convert string to list 
    myPreferences = string_to_list(myPreferences)
    print("MY PREF" , myPreferences)


    #convert string to int 
    for pref in prefereces: 
        for simPref in pref:
            simPref[1] = int(simPref[1]) 


    for pref in myPreferences:
        pref[1] = int(pref[1])
    


    
    similarityMatrix = []

    #we will be stroing the euclidean distance in the matrix of matching along with profile so a 2d list [[profile , euclidean distance] , [profile , euclidean distance] , ...
    for i in range(len(prefereces)):
        distanceValue = euclideanFormula(myPreferences , prefereces[i])
        ratingAdded =  distanceValue-allProfles[i].rating *.04 
        similarityMatrix.append([allProfles[i] ,ratingAdded ])


    #sort the matrix of matching on base of of second element of each list 
    
    similarityMatrix = sortMatrix(similarityMatrix)

    print("2d matrix" , similarityMatrix)
    
    matchingProfile = getListOfProfiles(similarityMatrix)

    
    return matchingProfile
