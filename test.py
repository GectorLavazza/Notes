a = 'qwertyuiopasdfghjklzxcvbnm'
for s in a:
    print(f"pygame.K_{s}: '{s}',")
for s in a:
    print(f"pygame.K_{s.capitalize()}: '{s.capitalize()}',")
