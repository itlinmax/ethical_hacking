import os
import configparser
from collections import namedtuple


def get_linux_saved_wifi_passwords(verbose=1):
    network_connections_path = "/etc/NetworkManager/system-connections/"
    fields = ["ssid", "auth-alg", "key-mgmt", "psk"]
    Profile = namedtuple("Profile", [f.replace("-", "_") for f in fields])
    profiles = []
    for file in os.listdir(network_connections_path):
        data = {k.replace("-", "_"): None for k in fields}
        config = configparser.ConfigParser()
        config.read(os.path.join(network_connections_path, file))
        for _, section in config.items():
            for k, v in section.items():
                if k in fields:
                    data[k.replace("-", "_")] = v
        profile = Profile(** data)
        if verbose >= 1:
            print_linux_profile(profile)
        profiles.append(profile)
    return profiles


def print_linux_profile(profile):
    print(f"{str(profile.ssid):25}{str(profile.auth_alg):5}{str(profile.key_mgmt):10}{str(profile.psk):50}")


def print_linux_profiles(verbose):
    print("SSID AUTH KEY-MGMT PSK")
    get_linux_saved_wifi_passwords(verbose)


def print_profiles(verbose=1):
    if os.name == "posix":
        print_linux_profiles(verbose)


if __name__ == "__main__":
    print_profiles()
