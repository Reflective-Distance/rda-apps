from utils.env_builder import EnvBuilder
import os

class Environment:
    """Singleton class to ensure environment is only configured once."""
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Environment, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Skip initialization if already done
        if self._initialized:
            return
            
        # Set flag first to prevent recursion in case of circular imports
        self.__class__._initialized = True
        
        # Configure environment
        EnvBuilder().with_defaults().build()
        
        # Set an environment flag to indicate we're configured
        os.environ["ENV_INITIALIZED"] = "true"
    
    @classmethod
    def is_initialized(cls):
        """Check if environment has been initialized."""
        return cls._initialized
    
    @classmethod
    def require_initialization(cls):
        """Ensure environment is initialized by creating an instance if needed."""
        if not cls._initialized:
            cls()


# Initialize environment on module import
environment = Environment()

# Public function to check/ensure initialization
def ensure_environment_initialized():
    """Ensure environment is initialized, creating it if necessary."""
    Environment.require_initialization()
    return Environment.is_initialized()