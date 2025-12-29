"""
Простой запуск игры.
"""

print("=" * 50)
print("ЗАПУСК DINO GAME")
print("=" * 50)
print("Управление:")
print("  SPACE - прыжок / начать игру")
print("  ESC - выход")
print("-" * 30)

try:
    from game.main import Game

    game = Game()
    game.run()
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback

    traceback.print_exc()
    input("\nНажмите Enter для выхода...")
