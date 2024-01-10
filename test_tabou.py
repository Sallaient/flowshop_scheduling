import tabou

path = "tai01.txt"
for i in range(10):
    tabou.tabouFromFile(path, maxTabou=50, printOrdo=False)