from dataprofile import Profiler
from ENV import Data_PATH, Unified_PATH, Trimmed_PATH

using_PATH = Trimmed_PATH
profiler = Profiler(using_PATH)
profiler.full_profile(if_print_profile=True)