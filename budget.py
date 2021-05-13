class Category(object):
  def __init__(self, category_name):
    self.category_name = category_name
    self.ledger = []
  
  def get_balance(self):
    amount = 0
    for e in self.ledger:
      amount += e["amount"]
    return amount
  
  def check_funds(self, target):
    current_account = self.get_balance()
    if target > current_account:
      return False
    
    return True
  
  def deposit(self, *args):
    amount = args[0]

    if len(args) > 1:
      description = args[1]
    else:
      description = ""
    
    self.ledger.append({"amount":amount, "description":description})
  
  def withdraw(self, *args):
    amount = args[0]

    if len(args) > 1:
      description = args[1]
    else:
      description = ""
    
    enough = self.check_funds(amount)
    if enough:
      self.ledger.append({"amount":-amount, "description":description})
      return True
    
    return False
  
  def transfer(self, amount, target_category):
        
    enough = self.check_funds(amount)
    if enough:
      description = "Transfer to {}".format(target_category.category_name)

      self.ledger.append({"amount":-amount, "description":description})

      other_description = "Transfer from {}".format(self.category_name)

      target_category.ledger.append({"amount":amount, "description":other_description})

      return True
    
    return False

  def show_withdrawls(self):
    taken = 0

    for e in self.ledger:
      if e["amount"] < 0:
        taken += e["amount"]
    
    return taken
  
  def __str__(self):
    r_string = ""
    r_string += self.category_name.center(30, "*")
    r_string += "\n"
    for e in self.ledger:
      e_string = e["description"].ljust(30, " ")
      e_2 = "{:.2f}".format(e["amount"])

      e_amount = e_2.rjust(30, " ")

      e_final = ""
      for i in range(30):
        if i < 23:
          e_final += e_string[i]
        else:
          e_final += e_amount[i]
      
      r_string += e_final
      r_string += "\n"
    
    balance = "{:.2f}".format(self.get_balance())    
    r_string += "Total: {}".format(balance)
    return r_string


def create_spend_chart(categories):

  x_length = len(categories) + 2

  y_length = 12

  longest = 0
  adding = []

  total_spending = 0

  for c in categories:
    c_name = c.category_name
    if len(c_name) > longest:
      longest = len(c_name)
    
    withdrawn = c.show_withdrawls()

    adding.append({"withdrawn":withdrawn, "c_name":c_name})
    total_spending += withdrawn
  
  for c in adding:
    percent = int(c["withdrawn"] / total_spending * 10.0)
    c["percent"] = percent
  
  y_length += longest

  d = {}
  
  for n in range(y_length):

    if n == 11:
      d[(x_length, n)] = "-"
      d[(0, n)] = "   "
      d[(1, n)] = " "

    elif n < 11:
      d[(x_length, n)] = " "
      d[(0, n)] = str((10 - n) * 10).rjust(3, " ")
      d[(1, n)] = "|"
    else:
      d[(x_length, n)] = " "
      d[(0, n)] = "   "
      d[(1, n)] = " "
    
    if n < y_length - 1:
      d[(x_length + 1, n)] = "\n"


  for a in range(len(adding)):
    a_entry = adding[a]
    a_name = a_entry["c_name"]
    a_len = len(a_name)

    adding_percent = 10 - a_entry["percent"]

    for t in range(y_length):
      d[(a + 2, 11)] = "---"
      if t < a_len:
        d[(a + 2, 12 + t)] = " {} ".format(a_name[t])
      else:
        d[(a + 2, 12 + t)] = "   "
    
    for ty in range(11):
      if ty >= adding_percent:
        d[(a + 2, ty)] = " o "
      else:
        d[(a + 2, ty)] = "   "
    
  output_string = "Percentage spent by category\n"
  for y in range(y_length):
    for x in range(x_length + 2):
      output = d.get((x, y))
      if output:
        output_string += output
    
  return output_string



