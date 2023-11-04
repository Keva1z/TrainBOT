import random
from database.manager import database, User

class Exercise():
    def __init__(self, name: str, details: str, pod: int, pov: list):
        self.name = name
        self.details = details
        self.pod = pod
        self.pov = f"{pov[0]} {pov[1]}"
        
    def __repr__(self) -> str:
        text = f"""<b>Занятие:</b> <u>{self.name}</u>
<b>Детали:</b> {self.details}
<b>Подходов:</b> <u>{self.pod}</u>
<b>Повторения:</b> <u>{self.pov}</u>"""
        alt = f"Ex({self.name})"
        return text
        
class Trainer():
    def __init__(self):
        self.path = "exercises.json"
        self.last_path = "exercises.json"
        self.allowed_days = ["legs", "back", "hands", "press", "warmup"]
        self.tips = [
            "Пейте больше воды, норма 2 литра в день!",
            "Ешьте меньше мучного, но немного сладкого иногда можно :)",
            "Грызть гранит науки - не самая вкусная еда, лучше есть овощи",
            "Чаще разминайтесь если долго сидите!",
            "Разминайтесь перед тренировкой, а то сломаетесь, потом мне вас собирать что ли?",
            "Если вам становиться не хорошо - лучше отложить тренировку на потом",
            "Не забывайте отдыхать между подходами, норма отдыха между подходами - 3 минуты",
            "Волосы могут попасть вам в глаза, завязывайте их в хвост",
            "Не перенагружайте свое тело! Если у вас тяжелая тренировка, занимайтесь раз в два-три дня",
            "Супер смешное видео с котятами -> https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        ]
    
    async def get_tip(self):
        return random.choice(self.tips)
    
    async def _load_last_plan(self, user: User.USER):
        if user.current_plan in user.plans:
            workout_list = []
            plan = user.plans[user.current_plan]
            for name in plan:
                ex = plan[name]
                e = Exercise(name, ex["details"], ex["approaches"], ex["repeats"])
                workout_list.append(e)
            user.task_list = workout_list
            await database.user.save(user)
        else:
            return False
        
    async def _load_plan(self, plan: str, user: User.USER):
        if plan in user.plans:
            if len(user.plans[plan]) > 0:
                if len(user.plans[plan]) >= 5:
                    workout_list = []
                    for name in user.plans[plan]:
                        ex = user.plans[plan][name]
                        e = Exercise(name, ex["details"], ex["approaches"], ex["repeats"])
                        workout_list.append(e)
                    user.current_plan = plan
                    user.task_list = workout_list
                    await database.user.save(user)
                
                    return (True, None)
                else:
                    return (False, f"В плане <b>'{plan}'</b> меньше 5 заданий!")
            else:
                return (False, f"В плане <b>'{plan}'</b> нет заданий!")
        else:
            return (False, f"Плана <b>'{plan}'</b> не существует!")
                
    async def get_exercise(self, user: User.USER):
        if user.task_list != []: 
            task_id = user.task_list.index(random.choice(user.task_list))
            task = user.task_list[task_id]
            user.task_list.remove(task)
            await database.user.save(user)
            return task
        else:
            return None

