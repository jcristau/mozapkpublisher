import pytest

from mozapkpublisher.exceptions import WrongArgumentGiven
from mozapkpublisher.get_apk import GetAPK

VALID_CONFIG = {'version': '50.0b8'}
get_apk = GetAPK(VALID_CONFIG)


def test_mutually_exclusive_group():
    with pytest.raises(WrongArgumentGiven):
        GetAPK({'clean': True, 'version': True})

    with pytest.raises(WrongArgumentGiven):
        GetAPK({'clean': True, 'latest_nightly': True})

    with pytest.raises(WrongArgumentGiven):
        GetAPK({'version': True, 'latest_nightly': True})

    with pytest.raises(WrongArgumentGiven):
        GetAPK({'latest_nightly': True, 'latest_aurora': True})


def test_generate_url():
    assert GetAPK({'latest_nightly': True}).generate_url('52.0a1', None, 'multi', 'x86', 'i386') == \
        'https://ftp.mozilla.org/pub/mobile/nightly/latest-mozilla-central-android-x86/fennec-52.0a1.multi.android-i386'

    assert GetAPK({'latest_aurora': True}).generate_url('51.0a2', None, 'en-US', 'api-15', 'arm') == \
        'https://ftp.mozilla.org/pub/mobile/nightly/latest-mozilla-aurora-android-api-15/fennec-51.0a2.en-US.android-arm'

    assert GetAPK({'version': '50.0b8'}).generate_url('50.0b8', 1, 'multi', 'api-15', 'arm') == \
        'https://ftp.mozilla.org/pub/mobile/candidates/50.0b8-candidates/build1/android-api-15/multi/fennec-50.0b8.multi.android-arm'


def test_get_arch_file():
    assert get_apk.get_arch_file('arm') == 'arm'
    assert get_apk.get_arch_file('x86') == 'i386'


def test_get_api_suffix():
    assert get_apk.get_api_suffix('arm') == ['api-15']
    assert get_apk.get_api_suffix('x86') == ['x86']


def test_get_common_file_name():
    assert get_apk.get_common_file_name('50.0b8', 'multi') == 'fennec-50.0b8.multi.android-'
    assert get_apk.get_common_file_name('51.0a2', 'en-US') == 'fennec-51.0a2.en-US.android-'
