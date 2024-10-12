CC=python3
FILE=main
CACHE_PATH=/Users/elisa/Library/Caches/fastf1

all: $(FILE) clear 
	@echo "Fermeture de l'application"

$(FILE): 
	@echo "Ouverture de l'application"
	$(CC) $(FILE).py

clear: 
	rm -rf $(CACHE_PATH)
	@echo "Supression du cache"

show: 
	ls $(CACHE_PATH)