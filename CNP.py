import random


f1 = open("Fete.txt", 'r')
f2 = open("Baieti.txt", 'r')
f3 = open("Nume.txt", 'r')
file = open("populatie.txt", "r")


class Node:
    def __init__(self, data: tuple):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def search(self, cnp: str) -> tuple:
        current = self.head
        index = 0
        while current:
            if current.data[0] == cnp:
                return index, current.data
            current = current.next
            index += 1
        return -1, None

    def append(self, data: tuple) -> None:
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def length(self) -> int:
        return self.size

    # functie ajutateoare pentru reprezentarea nodurilor la testare
    def __str__(self) -> str:
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        return " -> ".join(nodes)


def print_linkedlist_size(hash_table: dict) -> None:
    """
    Printeaza lungimea fiecarei liste simplu inlantuite pentru testare
    """
    for i in range(1000):  # Assuming the hash table has 1000 buckets
        linked_list = hash_table[i]
        if linked_list.length() > 0:
            print(f"Lungimea listei simplu inlantuite la pozitia {i}: {linked_list.length()}")
        else:
            print(f"Pozitia {i} este goala.")


def Generare_CNP(numar: int):
    populatie = file.readlines()
    JJ = 1
    counter = 0  # Contor pentru numărul de CNP-uri generate

    fete = f1.read().split()
    baieti = f2.read().split()
    nume_familii = f3.read().split()

    with open("CNP.txt", "w") as cnp_file:
        for element in range(numar):
            for i in populatie:
                reg_trei_simpla = (numar * int(i)) // 20000000
                if JJ == 53:
                    break
                for item in range(reg_trei_simpla):
                    if counter >= numar:
                        return

                    control = 0
                    S1 = random.randint(1, 100)
                    AA_raport = random.randint(0, 100)

                    if S1 <= 49 and AA_raport > 24:
                        S = 1
                    elif S1 <= 49 and AA_raport <= 24:
                        S = 5
                    elif S1 > 49 and AA_raport > 24:
                        S = 2
                    else:
                        S = 6
                    if S in [1, 2]:
                        AA = random.randint(0, 99)
                    else:
                        AA = random.randint(0, 24)
                    if AA < 10:
                        AA = f'0{AA}'
                    LL = random.randint(1, 12)
                    if LL < 10:
                        LL = f'0{LL}'
                    if int(LL) in [1, 3, 5, 7, 8, 10, 12]:
                        ZZ = random.randint(1, 31)
                    elif int(LL) in [4, 6, 9, 11]:
                        ZZ = random.randint(1, 30)
                    else:
                        ZZ = random.randint(1, 28)
                    if ZZ < 10:
                        ZZ = f'0{ZZ}'

                    JJ_str = f"{JJ:02}"

                    nnn = random.randint(1, 999)
                    if nnn < 10:
                        nnn = f'00{nnn}'
                    elif nnn < 100:
                        nnn = f'0{nnn}'
                    else:
                        nnn = str(nnn)

                    cnp = f'{S}{AA}{LL}{ZZ}{JJ_str}{nnn}'

                    constant = "279146358279"
                    for i in range(12):
                        control += int(cnp[i]) * int(constant[i])
                    control_digit = control % 11
                    if control_digit == 10:
                        control_digit = '1'
                    cnp = cnp + str(control_digit)

                    CNP_nume = [cnp]
                    if S % 2 == 0:
                        CNP_nume.append(random.choice(fete))
                    else:
                        CNP_nume.append(random.choice(baieti))

                    CNP_nume.append(random.choice(nume_familii))

                    complet = " ".join(CNP_nume)
                    cnp_file.write(f"{complet}\n")

                    counter += 1  # Incrementăm contorul

                JJ += 1


def Generare_Hash(cnp: str) -> int:
    prime = 31
    hash_val = 0
    for i, caracter in enumerate(cnp):
        hash_val += ord(caracter) * (prime ** i)
    return hash_val % 1000


def HashTable() -> dict:
    hash_table = {i: LinkedList() for i in range(1000)}
    with open("CNP.txt", "r") as f:
        for line in f:
            cnp, prenume, nume = line.split()
            full_name = f"{prenume} {nume}"
            h = Generare_Hash(cnp)
            hash_table[h].append([cnp, full_name])

    return hash_table


def Cautare_CNP(cnp: str, hash_table: dict) -> int:
    h = Generare_Hash(cnp)
    linked_list = hash_table[h]
    index, result = linked_list.search(cnp)

    if index != -1:
        return index + 1
    else:
        return -1


def random_CNP(file_path: str, count: int) -> list:
    with open(file_path, 'r') as f:
        cnp_list = [line.split()[0] for line in f]
    return random.sample(cnp_list, count)


if __name__ == '__main__':
    # Generarea celor 1M CNP - doar când e nevoie
    """
 !!!!!   Dupa popularea file-ului CNP.txt comentati afara Generare_CNP(1000000), sa nu mai genereze CNP din nou   !!!!!
    """
    Generare_CNP(1000000)

    # Generare hastable pe baza fișierului CNP.txt existent
    hash_table = HashTable()

    # Selectarea a 1000 de CNP-uri din lista pentru căutare
    random_CNPs = random_CNP("CNP.txt", 1000)

    # Printarea fiecarui Bucket - doar pentru testare
    # print_linkedlist_size(hash_table)

    # Căutarea CNP-urilor și analiza iteratiilor necesare
    total_iterations = 0
    for cnp in random_CNPs:
        iterations = Cautare_CNP(cnp, hash_table)
        total_iterations += iterations if iterations != -1 else 0

    print(f"Iterațiile necesare pentru regăsirea CNP-urilor: {total_iterations}")

