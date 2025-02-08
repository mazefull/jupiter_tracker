# jupiter_tracker
DEV_STACK: 
&backend.services: FastAPI + aiogram
&backend.db: sqlalchemy(postgres)
&frontend.base: reactJS
&frontend.components: tailwindcss, antdesign

&architecture:
input: 
frontend >> FastAPI >> backend
aiogram >> TelegramAPI >> backend ?

notify:
frontend.notify
telegram.bot.notify

uiux:
frontend
telegram.bot

roadmap:
rewrite architecture to oniontype(backend)
UNION jupiter.legacy(telegram) to backend
build authorization ?JWT ?(cookie or headers)
rewrite frontend.imports to simply type

.stars:
authorization
frontend.dynamic_task_builder — need JS dynamic generation
frontend.menu ? use floatButtons
backend.access.service — need permissions model
backend.service.aura_data_fixer ?onCreate or ?onReturnTask

