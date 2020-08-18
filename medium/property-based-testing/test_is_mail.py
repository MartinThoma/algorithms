# Third party modules
import hypothesis.strategies as s
import mpu.string  # Martins Python Utilities
from hypothesis import given


@given(s.emails())
def test_is_email(email):
    assert mpu.string.is_email(email), f"is_email({email}) returned False"


@given(s.ip_addresses(v=4))
def test_is_ipv4(ip):
    assert mpu.string.is_ipv4(str(ip)), f"is_ipv4({ip}) returned False"
