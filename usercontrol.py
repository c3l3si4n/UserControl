import time, mysql.connector, sys, itertools, threading, configparser
done = False

if len(sys.argv) < 2:
    print(
        """
    choose your mode:
    enable
    disable
    """
       
    )
    mode = input('option: ')
else:
    mode = sys.argv[1]
if (mode != "enable") and (mode != "disable"):
    print(
        """
    invalid argument, did you type something wrong?
    """
    )
    sys.exit()

operacao = 0

if mode == "enable":
    operacao = 0
else:
    operacao = 1


print(" ")
if operacao:
    print("disabling account:")
else:
    print("enabling account:")


name = input("username: ")


print("")


def animate():
    for c in itertools.cycle(["|", "/", "-", "\\"]):
        if done:
            break
        sys.stdout.write("\rloading " + c)
        sys.stdout.flush()
        time.sleep(0.05)

t = threading.Thread(target=animate)
t.start()

config = configparser.ConfigParser()
config.read('config.ini')

if (config['mysql']['address'] == '1.1.1.1'):
    print('\r                       ')
    print('\ryou need to edit the config first!')
    done = True
    exit(0)

print (config['mysql'][''])
cnx = mysql.connector.connect(
    user=config['mysql']['username'],
    password=config['mysql']['password'],
    host=config['mysql']['address'],
    database=config['mysql']['database'],
    use_pure=True
)


query = """SELECT hwid_atual FROM loader WHERE name = '%s'"""

cursor = cnx.cursor()
cursor.execute(query % name)

if not cursor.fetchone():
    done = True
    print("\r            ")
    print("\rerror:  username non existent")
    sys.exit()
cursor.execute(query % name)
row1temp = cursor.fetchone()

row1 = ""
row1 = format(row1temp[0])


print("\r              ")
print("\ruser hwid: %s" % row1)
query = """UPDATE loader SET hwid = ("%s") where name = "%s";"""
cursor.execute(query % (row1, name))


if operacao:
    query = """UPDATE loader SET ativado = 'false' where name = '%s';"""
else:
    query = """UPDATE loader SET ativado = 'true' where name = '%s';"""

cursor.execute(query % name)
cnx.commit()
done = True
print("\r             ")
if operacao:
    print("\ruser disabled with success!")
else:
    print("\ruser enabled with success!")
