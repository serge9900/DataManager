import re
import datetime

#Validation function for Name, Last name, Patronymic.
def isValidName(name):
    if name:
      if not name.isalpha():
          return False
      elif not name[0].isupper():
          return False     
      else:
          return True
    else:
      return False

#Validation function for birth date.
def isValidBirthDate(date):
    if date:
      try:
        datetime.datetime.strptime(date,"%Y/%m/%d")
        return True
      except:
        try:
          datetime.datetime.strptime(date,"%d/%m/%Y")
          return True
        except:
          try:
            datetime.datetime.strptime(date,"%m/%d/%Y")
            return True
          except:
            return False
    else:
      return True

#Validation function for Phone number.
def isValidPhoneNumber(number):
    if number:
      if len(number) == 12 and number.startswith("+374") and number[1:].isnumeric():
          return True
      else:
          return False
    else:
      return False

#Validation function for Email.
def isValidEmail(mail):
    if mail:
      invalidCharacters = ")(][}{><,?/\+:;'\"|~`!#$%^&*= "
      for sign in invalidCharacters:
        if sign in mail:
            return False

      if mail.startswith("-") or mail.startswith("_") or mail.startswith("@") or\
          mail.startswith(".") or not mail.islower() or mail.count("@") != 1:
          return False   
      else:
          domainName = mail[mail.index("@")+1:]
          if domainName.count(".") != 1 or domainName.count("_") != 0 or domainName.count("-") != 0:
              return False
          else:
              return True
    else:
      return False

def isValidPrice(price):
    if price:
      num_format = re.compile(r"^\d\d*[,]?\d*[,]?\d*[.,]?\d*\d$")
      it_is = re.match(num_format,str(price))

      if it_is:
        return True
      else:
        return False
    else:
      return False