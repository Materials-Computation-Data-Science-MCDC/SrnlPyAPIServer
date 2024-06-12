# import logging
# import time
# from glasspy.data import SciGlass
#
# # Configure the logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# class SciGlassService:
#     def __init__(self, elements_cfg=None, properties_cfg=None, compounds_cfg=None):
#         start_time = time.time()  # Start the timer
#         #self.source = SciGlass(elements_cfg=elements_cfg, properties_cfg=properties_cfg, compounds_cfg=compounds_cfg)
#         self.source = SciGlass()
#         end_time = time.time()  # End the timer
#         load_time = end_time - start_time  # Calculate the duration
#         logger.info(f"SciGlass data loaded in {load_time:.2f} seconds")
#
#     def get_data(self):
#         return self.source.data
#
# # Example configuration
# all_properties_except_Tg = SciGlass.available_properties()
# all_properties_except_Tg.remove("Tg")
#
# config_el = {
#     "drop": ["Ag", "Au", "Mg", "Na"],
# }
#
# config_prop = {
#     "keep": ["Tg"],
#     "drop": all_properties_except_Tg,
# }
#
# config_comp = {}
#
# # Instantiate the service with configurations
# sci_glass_service = SciGlassService()
