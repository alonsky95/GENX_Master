## device_factory.py is a utility object that specifies how device objects are to be created

@dataclass
class DutConfig:
    device_type: str
    # something else?


class DeviceFactory:
    @staticmethod
    def new_device(DutConfig):
        if DutConfig.device_type == 'Prion':
            return Prion