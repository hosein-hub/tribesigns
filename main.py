from functions import get_links,get_data




if __name__ == '__main__':
    file1 = open('links.txt', 'r')
    Lines = file1.readlines()
    for line in Lines:
        print(line.strip())
        get_data(line.strip())
