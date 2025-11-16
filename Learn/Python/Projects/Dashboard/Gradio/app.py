# Browse : http://127.0.0.1:7860/

import logging
import warnings
import dashboard_actions as dashboard

warnings.filterwarnings("ignore", category=FutureWarning, module="seaborn")

# Exception in ASGI application - Fixed With downgrading pydantic=2.10.6
if __name__ == "__main__":
   _app = dashboard.create_dashboard()
   _app.launch(share=False)