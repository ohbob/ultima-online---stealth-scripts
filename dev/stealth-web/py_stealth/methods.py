from __future__ import division

import datetime as _datetime
import struct as _struct
import time as _time

from ._datatypes import *
from ._protocol import EVENTS_NAMES as _EVENTS_NAMES
from ._protocol import ScriptMethod as _ScriptMethod
from ._protocol import get_connection as _get_connection
from .utils import ddt2pdt as _ddt2pdt
from .utils import pdt2ddt as _pdt2ddt
from .utils import iterable as _iterable

_clear_event_callback = _ScriptMethod(7)  # ClearEventProc
_clear_event_callback.argtypes = [_ubyte]  # EventIndex

_set_event_callback = _ScriptMethod(11)  # SetEventProc
_set_event_callback.argtypes = [_ubyte]  # EventIndex


def SetEventProc(EventName, Callback=None):
    conn = _get_connection()
    try:
        index = _EVENTS_NAMES.index(EventName.lower())
    except ValueError:
        raise ValueError('Unknown event "' + EventName + '".')
    # clear event
    if Callback is None:
        _clear_event_callback(index)
        # conn.callbacks[index] = None
    # set event
    else:
        if conn.callbacks[index] is None:
            _set_event_callback(index)
        conn.callbacks[index] = Callback


_connected = _ScriptMethod(9)  # GetConnectedStatus
_connected.restype = _bool


def Connected():
    return _connected()


_add_to_system_journal = _ScriptMethod(10)  # AddToSystemJournal
_add_to_system_journal.argtypes = [_str]  # Text


def AddToSystemJournal(*args, **kwargs):
    sep = kwargs.pop('sep', ', ')
    end = kwargs.pop('end', '')
    s_args = sep.join((str(arg) for arg in args))
    s_kwargs = sep.join((str(k) + '=' + str(v) for k, v in kwargs.items()))
    text = s_args + (sep if s_args and s_kwargs else '') + s_kwargs + end
    _add_to_system_journal(text)


_get_stealth_info = _ScriptMethod(12)  # GetStealthInfo
_get_stealth_info.restype = _buffer  # TAboutData


def GetStealthInfo():
    data = _get_stealth_info()
    result = dict()
    result['StealthVersion'] = _struct.unpack('<3H', data[4:10])
    result['Build'] = _struct.unpack('<H', data[10:12])[0]
    result['BuildDate'] = _ddt2pdt(_struct.unpack('<d', data[12:20])[0])
    result['GITRevNumber'] = _struct.unpack('<H', data[20:22])[0]
    result['GITRevision'] = _str.from_buffer(data[22:]).value
    return result


_connect = _ScriptMethod(45)  # Connect


def Connect():
    _connect()


_disconnect = _ScriptMethod(46)  # Disconnect


def Disconnect():
    _disconnect()


_set_pause_on_disc = _ScriptMethod(24)  # SetPauseScriptOnDisconnectStatus
_set_pause_on_disc.argtypes = [_bool]  # Value


def SetPauseScriptOnDisconnectStatus(Value):
    _set_pause_on_disc(Value)


_get_pause_on_disc = _ScriptMethod(23)  # GetPauseScriptOnDisconnectStatus
_get_pause_on_disc.restype = _bool


def GetPauseScriptOnDisconnectStatus():
    return _get_pause_on_disc()


_set_reconnector = _ScriptMethod(22)  # SetARStatus
_set_reconnector.argtypes = [_bool]  # Value


def SetARStatus(Value):
    _set_reconnector(Value)


_get_reconnector = _ScriptMethod(21)  # GetARStatus
_get_reconnector.restype = _bool


def GetARStatus():
    return _get_reconnector()


_get_self_name = _ScriptMethod(19)  # GetCharName
_get_self_name.restype = _str


def CharName():
    return _get_self_name()


_change_profile = _ScriptMethod(20)  # ChangeProfile
_change_profile.restype = _int
_change_profile.argtypes = [_str]  # PName


def ChangeProfile(PName):
    return _change_profile(PName)


_change_profile_ex = _ScriptMethod(352)  # ChangeProfileEx
_change_profile_ex.restype = _int
_change_profile_ex.argtypes = [_str,  # PName
                               _str,  # ShardName
                               _str]  # CharName


def ChangeProfileEx(PName, ShardName, CharName):
    return _change_profile_ex(PName, ShardName, CharName)


_get_profile_name = _ScriptMethod(8)  # ProfileName
_get_profile_name.restype = _str


def ProfileName():
    return _get_profile_name()


_get_self_id = _ScriptMethod(14)  # GetSelfID
_get_self_id.restype = _uint


def Self():
    return _get_self_id()


_get_self_sex = _ScriptMethod(25)  # GetSelfSex
_get_self_sex.restype = _ubyte


def Sex():
    return _get_self_sex()


_get_char_title = _ScriptMethod(26)  # GetCharTitle
_get_char_title.restype = _str


def GetCharTitle():
    return _get_char_title()


_get_gold_count = _ScriptMethod(27)  # GetSelfGold
_get_gold_count.restype = _ushort


def Gold():
    return _get_gold_count()


_get_armor_points = _ScriptMethod(28)  # GetSelfArmor
_get_armor_points.restype = _ushort


def Armor():
    return _get_armor_points()


_get_weight = _ScriptMethod(29)  # GetSelfWeight
_get_weight.restype = _ushort


def Weight():
    return _get_weight()


_get_max_weight = _ScriptMethod(30)  # GetSelfMaxWeight
_get_max_weight.restype = _ushort


def MaxWeight():
    return _get_max_weight()


_get_world_number = _ScriptMethod(18)  # GetWorldNum
_get_world_number.restype = _ubyte


def WorldNum():
    return _get_world_number()


_get_self_race = _ScriptMethod(31)  # GetSelfRace
_get_self_race.restype = _ubyte


def Race():
    return _get_self_race()


_get_max_pets = _ScriptMethod(32)  # GetSelfPetsMax
_get_max_pets.restype = _ubyte


def MaxPets():
    return _get_max_pets()


_get_pets_count = _ScriptMethod(33)  # GetSelfPetsCurrent
_get_pets_count.restype = _ubyte


def PetsCurrent():
    return _get_pets_count()


_get_fire_resist = _ScriptMethod(34)  # GetSelfFireResist
_get_fire_resist.restype = _ushort


def FireResist():
    return _get_fire_resist()


_get_cold_resist = _ScriptMethod(35)  # GetSelfColdResist
_get_cold_resist.restype = _ushort


def ColdResist():
    return _get_cold_resist()


_get_poison_resist = _ScriptMethod(36)  # GetSelfPoisonResist
_get_poison_resist.restype = _ushort


def PoisonResist():
    return _get_poison_resist()


_get_energy_resist = _ScriptMethod(37)  # GetSelfEnergyResist
_get_energy_resist.restype = _ushort


def EnergyResist():
    return _get_energy_resist()


_get_last_connection_time = _ScriptMethod(38)  # GetConnectedTime
_get_last_connection_time.restype = _double


def ConnectedTime():
    return _ddt2pdt(_get_last_connection_time())


_get_last_disconnection_time = _ScriptMethod(39)  # GetDisconnectedTime
_get_last_disconnection_time.restype = _double


def DisconnectedTime():
    return _ddt2pdt(_get_last_disconnection_time())


_get_last_opened_container = _ScriptMethod(40)  # GetLastContainer
_get_last_opened_container.restype = _uint


def LastContainer():
    return _get_last_opened_container()


_get_last_targeted_object = _ScriptMethod(41)  # GetLastTarget
_get_last_targeted_object.restype = _uint


def LastTarget():
    return _get_last_targeted_object()


_get_last_attacked_object = _ScriptMethod(42)  # GetLastAttack
_get_last_attacked_object.restype = _uint


def LastAttack():
    return _get_last_attacked_object()


_get_last_status = _ScriptMethod(43)  # GetLastStatus
_get_last_status.restype = _uint


def LastStatus():
    return _get_last_status()


_get_last_used_object = _ScriptMethod(44)  # GetLastObject
_get_last_used_object.restype = _uint


def LastObject():
    return _get_last_used_object()


_get_buff_bar_info = _ScriptMethod(349)  # GetBuffBarInfo
_get_buff_bar_info.restype = _buffer  # TBuffBarInfo


def GetBuffBarInfo():
    result = []
    fmt = '<HdHII'
    size = _struct.calcsize(fmt)
    keys = ('Attribute_ID', 'TimeStart', 'Seconds', 'ClilocID1', 'ClilocID2')
    data = _get_buff_bar_info()
    if b'' == '':  # py2
        data = bytes(data)
    count = _uint.from_buffer(data)
    data = data[4:]
    for i in range(count):
        values = _struct.unpack(fmt, data[i * size:i * size + size])
        buff = dict(zip(keys, values))
        buff['TimeStart'] = _ddt2pdt(buff['TimeStart'])
        result.append(buff)
    return result


_get_shard_name = _ScriptMethod(47)  # GetShardName
_get_shard_name.restype = _str


def ShardName():
    return _get_shard_name()


_get_profile_shard_name = _ScriptMethod(343)  # GetProfileShardName
_get_profile_shard_name.restype = _str


def ProfileShardName():
    return _get_profile_shard_name()


_get_proxy_ip = _ScriptMethod(60)  # GetProxyIP
_get_proxy_ip.restype = _str


def ProxyIP():
    return _get_proxy_ip()


_get_proxy_port = _ScriptMethod(61)  # GetProxyPort
_get_proxy_port.restype = _ushort


def ProxyPort():
    return _get_proxy_port()


_is_proxy_using = _ScriptMethod(62)  # GetUseProxy
_is_proxy_using.restype = _bool


def UseProxy():
    return _is_proxy_using()


_get_backpack_id = _ScriptMethod(48)  # GetBackpackID
_get_backpack_id.restype = _uint


def Backpack():
    return _get_backpack_id()


def Ground():
    return 0


_get_char_strength = _ScriptMethod(49)  # GetSelfStr
_get_char_strength.restype = _int


def Str():
    return _get_char_strength()


_get_char_intelligence = _ScriptMethod(50)  # GetSelfInt
_get_char_intelligence.restype = _int


def Int():
    return _get_char_intelligence()


_get_char_dexterity = _ScriptMethod(51)  # GetSelfDex
_get_char_dexterity.restype = _int


def Dex():
    return _get_char_dexterity()


_get_char_hp = _ScriptMethod(52)  # GetSelfLife
_get_char_hp.restype = _int


def Life():
    return _get_char_hp()


def HP():
    return _get_char_hp()


_get_char_mana = _ScriptMethod(53)  # GetSelfMana
_get_char_mana.restype = _int


def Mana():
    return _get_char_mana()


_get_char_stamina = _ScriptMethod(54)  # GetSelfStam
_get_char_stamina.restype = _int


def Stam():
    return _get_char_stamina()


_get_char_max_hp = _ScriptMethod(55)  # GetSelfMaxLife
_get_char_max_hp.restype = _int


def MaxLife():
    return _get_char_max_hp()


def MaxHP():
    return _get_char_max_hp()


_get_char_max_mana = _ScriptMethod(56)  # GetSelfMaxMana
_get_char_max_mana.restype = _int


def MaxMana():
    return _get_char_max_mana()


_get_char_max_stamina = _ScriptMethod(57)  # GetMaxStam
_get_char_max_stamina.restype = _int


def MaxStam():
    return _get_char_max_stamina()


_get_char_luck = _ScriptMethod(58)  # GetSelfLuck
_get_char_luck.restype = _ushort


def Luck():
    return _get_char_luck()


_get_extended_info = _ScriptMethod(59)  # GetExtInfo
_get_extended_info.restype = _buffer  # TExtendedInfo


def GetExtInfo():
    keys = ('MaxWeight', 'Race', 'StatCap', 'PetsCurrent', 'PetsMax',
            'FireResist', 'ColdResist', 'PoisonResist', 'EnergyResist',
            'Luck', 'DamageMin', 'DamageMax', 'Tithing_points',
            'ArmorMax', 'fireresistMax', 'coldresistMax',
            'poisonresistMax', 'energyresistMax', 'DefenseChance',
            'DefensceChanceMax', 'Hit_Chance_Incr', 'Damage_Incr',
            'Swing_Speed_Incr', 'Lower_Reagent_Cost', 'Spell_Damage_Incr',
            'Faster_Cast_Recovery', 'Faster_Casting', 'Lower_Mana_Cost',
            'HP_Regen', 'Stam_Regen', 'Mana_Regen', 'Reflect_Phys_Damage',
            'Enhance_Potions', 'Strength_Incr', 'Dex_Incr', 'Int_Incr',
            'HP_Incr', 'Mana_Incr')
    fmt = '<HBH2B4Hh2Hi26H'
    data = _get_extended_info()
    if b'' == '':  # py2
        data = bytes(data)
    values = _struct.unpack(fmt, data)
    return dict(zip(keys, values))


_is_hidden = _ScriptMethod(63)  # GetHiddenStatus
_is_hidden.restype = _bool


def Hidden():
    return _is_hidden()


_is_poisoned = _ScriptMethod(64)  # GetPoisonedStatus
_is_poisoned.restype = _bool


def Poisoned():
    return _is_poisoned()


_is_paralyzed = _ScriptMethod(65)  # GetParalyzedStatus
_is_paralyzed.restype = _bool


def Paralyzed():
    return _is_paralyzed()


_is_dead = _ScriptMethod(66)  # GetDeadStatus
_is_dead.restype = _bool


def Dead():
    return _is_dead()


_get_warmode = _ScriptMethod(171)  # IsWarMode
_get_warmode.restype = _bool
_get_warmode.argtypes = [_uint]  # ObjID


def WarMode():
    return _get_warmode(Self())


_get_war_target = _ScriptMethod(67)  # GetWarTargetID
_get_war_target.restype = _uint


def WarTargetID():
    return _get_war_target()


_set_warmode = _ScriptMethod(68)  # SetWarMode
_set_warmode.argtypes = [_bool]  # Value


def SetWarMode(Value):
    _set_warmode(Value)


_attack = _ScriptMethod(69)  # Attack
_attack.argtypes = [_uint]  # AttackedID


def Attack(AttackedID):
    _attack(AttackedID)


_use_self_paperdoll = _ScriptMethod(70)  # UseSelfPaperdollScroll


def UseSelfPaperdollScroll():
    _use_self_paperdoll()


_use_paperdoll = _ScriptMethod(71)  # UseOtherPaperdollScroll
_use_paperdoll.argtypes = [_uint]  # ID


def UseOtherPaperdollScroll(ID):
    _use_paperdoll(ID)


_target_id = _ScriptMethod(72)  # GetTargetID
_target_id.restype = _uint


def TargetID():
    return _target_id()


def TargetPresent():  # GetTargetStatus
    return bool(_target_id())


def WaitForTarget(MaxWaitTimeMS):
    time = _time.time()
    while not _target_id() and time + MaxWaitTimeMS / 1000 > _time.time():
        Wait(10)
    return time + MaxWaitTimeMS / 1000 > _time.time()


_cancel_target = _ScriptMethod(73)  # CancelTarget


def CancelTarget():
    _cancel_target()
    while _target_id():
        Wait(10)


_target_to_object = _ScriptMethod(74)  # TargetToObject
_target_to_object.argtypes = [_uint]  # ObjectID


def TargetToObject(ObjectID):
    _target_to_object(ObjectID)


_target_xyz = _ScriptMethod(75)  # TargetToXYZ
_target_xyz.argtypes = [_ushort,  # X
                        _ushort,  # Y
                        _byte]  # Z


def TargetToXYZ(X, Y, Z):
    _target_xyz(X, Y, Z)


_target_tile = _ScriptMethod(76)  # TargetToTile
_target_tile.argtypes = [_ushort,  # TileModel
                         _ushort,  # X
                         _ushort,  # Y
                         _byte]  # Z


def TargetToTile(TileModel, X, Y, Z):
    _target_tile(TileModel, X, Y, Z)


_wait_target_object = _ScriptMethod(77)  # WaitTargetObject
_wait_target_object.argtypes = [_uint]  # ObjID


def WaitTargetObject(ObjID):
    _wait_target_object(ObjID)


_wait_target_tile = _ScriptMethod(78)  # WaitTargetTile
_wait_target_tile.argtypes = [_ushort,  # Tile
                              _ushort,  # X
                              _ushort,  # Y
                              _byte]  # Z


def WaitTargetTile(Tile, X, Y, Z):
    _wait_target_tile(Tile, X, Y, Z)


_wait_target_xyz = _ScriptMethod(79)  # WaitTargetXYZ
_wait_target_xyz.argtypes = [_ushort,  # X
                             _ushort,  # Y
                             _byte]  # Z


def WaitTargetXYZ(X, Y, Z):
    _wait_target_xyz(X, Y, Z)


_wait_target_self = _ScriptMethod(80)  # WaitTargetSelf


def WaitTargetSelf():
    _wait_target_self()


_wait_target_graphic = _ScriptMethod(81)  # WaitTargetType
_wait_target_graphic.argtypes = [_ushort]  # ObjType


def WaitTargetType(ObjType):
    _wait_target_graphic(ObjType)


_cancel_wait_target = _ScriptMethod(82)  # CancelWaitTarget


def CancelWaitTarget():
    _cancel_wait_target()


_wait_target_ground = _ScriptMethod(83)  # WaitTargetGround
_wait_target_ground.argtypes = [_ushort]  # ObjType


def WaitTargetGround(ObjType):
    _wait_target_ground(ObjType)


_wait_target_last = _ScriptMethod(84)  # WaitTargetLast


def WaitTargetLast():
    _wait_target_last()


_wait = _ScriptMethod(0)  # Wait


def Wait(WaitTimeMS):
    end = _time.time() + WaitTimeMS / 1000
    while _time.time() < end:
        _wait()  # pause script and event checks
        _time.sleep(0.010)
    else:
        _wait()  # condition does not work while delay is a very small number


_use_primary_ability = _ScriptMethod(85)  # UsePrimaryAbility


def UsePrimaryAbility():
    _use_primary_ability()


_use_secondary_ability = _ScriptMethod(86)  # UseSecondaryAbility


def UseSecondaryAbility():
    _use_secondary_ability()


_get_ability = _ScriptMethod(87)  # GetAbility
_get_ability.restype = _str


def GetActiveAbility():
    return _get_ability()


_toggle_fly = _ScriptMethod(88)  # ToggleFly


def ToggleFly():
    _toggle_fly()


_get_skill_id_from_socket = _ScriptMethod(89)  # GetSkillID
_get_skill_id_from_socket.restype = _int  # SkillID
_get_skill_id_from_socket.argtypes = [_str]  # SkillName


def _get_skill_id(name):
    skill_id = _get_skill_id_from_socket(name)
    if skill_id < 0:
        raise ValueError('Unknown skill name "' + name + '".')
    return skill_id


_use_skill = _ScriptMethod(90)  # UseSkill
_use_skill.argtypes = [_int]  # SkillID


def UseSkill(SkillName):
    _use_skill(_get_skill_id(SkillName))
    return True


_lock_skill = _ScriptMethod(91)  # ChangeSkillLockState
_lock_skill.argtypes = [_int,  # SkillID
                        _ubyte]  # SkillState


def ChangeSkillLockState(SkillName, skillState):
    _lock_skill(_get_skill_id_from_socket(SkillName), skillState)


def SetSkillLockState(SkillName, skillState):
    ChangeSkillLockState(SkillName, skillState)


_get_skill_cap = _ScriptMethod(92)  # GetSkillCap
_get_skill_cap.restype = _double
_get_skill_cap.argtypes = [_int]  # SkillID


def GetSkillCap(SkillName):
    return _get_skill_cap(_get_skill_id_from_socket(SkillName))


_get_skill_value = _ScriptMethod(93)  # GetSkillValue
_get_skill_value.restype = _double
_get_skill_value.argtypes = [_int]  # SkillID


def GetSkillValue(SkillName):
    return _get_skill_value(_get_skill_id_from_socket(SkillName))


_get_skill_current_value = _ScriptMethod(351)  # GetSkillCurrentValue
_get_skill_current_value.restype = _double
_get_skill_current_value.argtypes = [_int]  # SkillID


def GetSkillCurrentValue(SkillName):
    return _get_skill_current_value(_get_skill_id_from_socket(SkillName))


_request_virtues = _ScriptMethod(94)  # ReqVirtuesGump


def ReqVirtuesGump():
    _request_virtues()


_VIRTUES = {
    'compassion': 0x69,
    'honesty': 0x6A,
    'honor': 0x6B,
    'humility': 0x6C,
    'justice': 0x6D,
    'sacrifice': 0x6E,
    'spirituality': 0x6F,
    'valor': 0x70,
}

_use_virtue = _ScriptMethod(95)  # UseVirtue
_use_virtue.argtypes = [_uint]


def UseVirtue(VirtueName):
    if VirtueName.lower() not in _VIRTUES:
        error = 'UseVirtue error: Unknown name "' + VirtueName + '".'
        raise ValueError(error)
    _use_virtue(_VIRTUES[VirtueName.lower()])


_SPELLS = {
    # 1st circle
    'clumsy': 1,
    'create food': 2,
    'feeblemind': 3,
    'heal': 4,
    'magic arrow': 5,
    'night sight': 6,
    'reactive armor': 7,
    'weaken': 8,
    # 2nd circle
    'agility': 9,
    'cunning': 10,
    'cure': 11,
    'harm': 12,
    'magic trap': 13,
    'magic untrap': 14,
    'protection': 15,
    'strength': 16,
    # 3rd circle
    'bless': 17,
    'fireball': 18,
    'magic lock': 19,
    'poison': 20,
    'telekinesis': 21,
    'teleport': 22,
    'unlock': 23,
    'wall of stone': 24,
    # 4th circle
    'arch cure': 25,
    'arch protection': 26,
    'curse': 27,
    'fire field': 28,
    'greater heal': 29,
    'lightning': 30,
    'mana drain': 31,
    'recall': 32,
    # 5th circle
    'blade spirit': 33,
    'dispel field': 34,
    'incognito': 35,
    'magic reflection': 36,
    'spell reflection': 36,
    'mind blast': 37,
    'paralyze': 38,
    'poison field': 39,
    'summon creature': 40,
    # 6th circle
    'dispel': 41,
    'energy bolt': 42,
    'explosion': 43,
    'invisibility': 44,
    'mark': 45,
    'mass curse': 46,
    'paralyze field': 47,
    'reveal': 48,
    # 7th circle
    'chain lightning': 49,
    'energy field': 50,
    'flame strike': 51,
    'gate travel': 52,
    'mana vampire': 53,
    'mass dispel': 54,
    'meteor swarm': 55,
    'polymorph': 56,
    # 8th circle
    'earthquake': 57,
    'energy vortex': 58,
    'resurrection': 59,
    'summon air elemental': 60,
    'summon daemon': 61,
    'summon earth elemental': 62,
    'summon fire elemental': 63,
    'summon water elemental': 64,
    # Necromancy
    'animate dead': 101,
    'blood oath': 102,
    'corpse skin': 103,
    'curse weapon': 104,
    'evil omen': 105,
    'horrific beast': 106,
    'lich form': 107,
    'mind rot': 108,
    'pain spike': 109,
    'poison strike': 110,
    'strangle': 111,
    'summon familiar': 112,
    'vampiric embrace': 113,
    'vengeful spirit': 114,
    'wither': 115,
    'wraith form': 116,
    'exorcism': 117,
    # Paladin spells
    'cleanse by fire': 201,
    'close wounds': 202,
    'consecrate weapon': 203,
    'dispel evil': 204,
    'divine fury': 205,
    'enemy of one': 206,
    'holy light': 207,
    'noble sacrifice': 208,
    'remove curse': 209,
    'sacred journey': 210,
    # Bushido spells
    'honorable execution': 401,
    'confidence': 402,
    'evasion': 403,
    'counter attack': 404,
    'lightning strike': 405,
    'momentum strike': 406,
    # Ninjitsu spells
    'focus attack': 501,
    'death strike': 502,
    'animal form': 503,
    'ki attack': 504,
    'surprise attack': 505,
    'backstab': 506,
    'shadow jump': 507,
    'mirror image': 508,
    # Spellweaving spells
    'arcane circle': 601,
    'gift of renewal': 602,
    'immolating weapon': 603,
    'attunement': 604,
    'thunderstorm': 605,
    'nature fury': 606,
    'summon fey': 607,
    'summon fiend': 608,
    'reaper form': 609,
    'wildfire': 610,
    'essence of wind': 611,
    'dryad allure': 612,
    'ethereal voyage': 613,
    'word of death': 614,
    'gift of life': 615,
    'arcane empowerment': 616,
    # Mysticism spells
    'nether bolt': 678,
    'healing stone': 679,
    'pure magic': 680,
    'enchant': 681,
    'sleep': 682,
    'eagle strike': 683,
    'animated weapon': 684,
    'stone form': 685,
    'spell trigger': 686,
    'mass sleep': 687,
    'cleansing winds': 688,
    'bombard': 689,
    'spell plague': 690,
    'hail storm': 691,
    'nether cyclone': 692,
    'rising colossus': 693,
    # Shared Passives
    'enchanted summoning': 715,
    'enchanted_summoning': 715,
    'intuition': 718,
    'warriors gifts': 733,
    'warriors_gifts': 733,
    "warrior's gifts": 733,
    # Provocation
    'inspire': 701,
    'invigorate': 702,
    # Peacemaking
    'resilience': 703,
    'perseverance': 704,
    # Discordance
    'tribulation': 705,
    'despair': 706,
    # Magery
    'death_ray': 707,
    'death ray': 707,
    'ethereal_burst': 708,
    'ethereal burst': 708,
    'ethereal_blast': 708,
    'ethereal blast': 708,
    # Mysticism
    'nether_blast': 709,
    'nether blast': 709,
    'mystic_weapon': 710,
    'mystic weapon': 710,
    # Necromancy
    'command_undead': 711,
    'command undead': 711,
    'conduit': 712,
    # Spellweaving
    'mana_shield': 713,
    'mana shield': 713,
    'summon_reaper': 714,
    'summon reaper': 714,
    # Bushido
    'anticipate_hit': 716,
    'anticipate hit': 716,
    'warcry': 717,
    # Chivalry
    'rejuvenate': 719,
    'holy_fist': 720,
    'holy fist': 720,
    # Ninjitsu
    'shadow': 721,
    'white_tiger_form': 722,
    'white tiger form': 722,
    # Archery
    'flaming_shot': 723,
    'flaming shot': 723,
    'playing_the_odds': 724,
    'playing the odds': 724,
    # Fencing
    'thrust': 725,
    'pierce': 726,
    # Mace Fighting
    'stagger': 727,
    'toughness': 728,
    # Swordsmanship
    'onslaught': 729,
    'focused_eye': 730,
    'focused eye': 730,
    # Throwing
    'elemental_fury': 731,
    'elemental fury': 731,
    'called_shot': 732,
    'called shot': 732,
    # Parrying
    'shield_bash': 734,
    'shield bash': 734,
    'bodyguard': 735,
    'heighten_senses': 736,
    'heighten senses': 736,
    # Poisoning
    'tolerance': 737,
    'injected_strike': 738,
    'injected strike': 738,
    'potency': 739,
    # Wrestling
    'rampage': 740,
    'fists_of_fury': 741,
    'fists of fury': 741,
    'knockout': 742,
    # Animal Taming
    'whispering': 743,
    'boarding': 745,
    'combat_training': 744,
    'combat training': 744,
}


def _get_spell_id(name):
    name = name.lower()
    if name not in _SPELLS:
        raise ValueError('Unknown spell name "' + name + '".')
    return _SPELLS[name]


_cast_spell = _ScriptMethod(96)  # CastSpell
_cast_spell.argtypes = [_int]  # SpellID


def Cast(SpellName):
    _cast_spell(_get_spell_id(SpellName))
    return True


def CastToObj(SpellName, ObjID):
    _wait_target_object(ObjID)
    _cast_spell(_get_spell_id(SpellName))


def CastToObject(SpellName, ObjID):
    _wait_target_object(ObjID)
    _cast_spell(_get_spell_id(SpellName))


_is_active_spell_ability = _ScriptMethod(98)  # IsActiveSpellAbility
_is_active_spell_ability.restype = _bool
_is_active_spell_ability.argtypes = [_int]  # SpellName


def IsActiveSpellAbility(SpellName):
    return _is_active_spell_ability(_get_spell_id(SpellName))


_clear_catch_bag = _ScriptMethod(100)  # UnsetCatchBag


def UnsetCatchBag():
    _clear_catch_bag()


_set_catch_bag = _ScriptMethod(99)  # SetCatchBag
_set_catch_bag.argtypes = [_uint]  # ObjectID


def SetCatchBag(ObjectID):
    if ObjectID == 0:
        _clear_catch_bag()
        return 0
    elif not _is_object_exists(ObjectID):
        error = 'SetCatchBag Error: Object {} not found.'.format(hex(ObjectID))
        AddToSystemJournal(error)
        return 1
    else:
        _set_catch_bag(ObjectID)
        return 2


_use_object = _ScriptMethod(101)  # UseObject
_use_object.argtypes = [_uint]  # ObjectID


def UseObject(ObjectID):
    _use_object(ObjectID)


_use_type = _ScriptMethod(102)  # UseType
_use_type.restype = _uint
_use_type.argtypes = [_ushort,  # ObjType
                      _ushort]  # Color


def UseType(ObjType, Color):
    return _use_type(ObjType, Color)


def UseType2(ObjType):
    return _use_type(ObjType, 0xFFFF)


_use_from_ground = _ScriptMethod(103)  # UseFromGround
_use_from_ground.restype = _uint
_use_from_ground.argtypes = [_ushort,  # ObjType
                             _ushort]  # Color


def UseFromGround(ObjType, Color):
    return _use_from_ground(ObjType, Color)


_click_on_object = _ScriptMethod(104)  # ClickOnObject
_click_on_object.argtypes = [_uint]  # ObjectID


def ClickOnObject(ObjectID):
    if not _is_object_exists(ObjectID):
        err = 'ClickOnObject error: Object {} not found.'.format(hex(ObjectID))
        AddToSystemJournal(err)
    else:
        _click_on_object(ObjectID)


_get_found_index = _ScriptMethod(105)  # GetFoundedParamID
_get_found_index.restype = _int


def FoundedParamID():
    return _get_found_index()


def FoundParamID():
    return _get_found_index()


_get_last_line_serial = _ScriptMethod(106)  # GetLineID
_get_last_line_serial.restype = _uint


def LineID():
    return _get_last_line_serial()


_get_last_line_graphic = _ScriptMethod(107)  # GetLineType
_get_last_line_graphic.restype = _ushort


def LineType():
    return _get_last_line_graphic()


_get_last_line_name = _ScriptMethod(114)  # GetLineName
_get_last_line_name.restype = _str


def LineName():
    return _get_last_line_name()


_get_last_line_time = _ScriptMethod(108)  # GetLineTime
_get_last_line_time.restype = _double


def LineTime():
    return _ddt2pdt(_get_last_line_time())


_get_last_line_message_type = _ScriptMethod(109)  # GetLineMsgType
_get_last_line_message_type.restype = _ubyte


def LineMsgType():
    return _get_last_line_message_type()


_get_last_line_font_color = _ScriptMethod(110)  # GetLineTextColor
_get_last_line_font_color.restype = _ushort


def LineTextColor():
    return _get_last_line_font_color()


_get_last_line_font = _ScriptMethod(111)  # GetLineTextFont
_get_last_line_font.restype = _ushort


def LineTextFont():
    return _get_last_line_font()


_get_last_line_index = _ScriptMethod(112)  # GetLineIndex
_get_last_line_index.restype = _int


def LineIndex():
    return _get_last_line_index()


_get_last_line_count = _ScriptMethod(113)  # GetLineCount
_get_last_line_count.restype = _int


def LineCount():
    return _get_last_line_count()


_journal_ignore = _ScriptMethod(115)  # AddJournalIgnore
_journal_ignore.argtypes = [_str]  # Str


def AddJournalIgnore(Str):
    _journal_ignore(Str)


_clear_journal_ignore = _ScriptMethod(116)  # ClearJournalIgnore


def ClearJournalIgnore():
    _clear_journal_ignore()


_chat_ignore = _ScriptMethod(117)  # AddChatUserIgnore
_chat_ignore.argtypes = [_str]  # User


def AddChatUserIgnore(User):
    _chat_ignore(User)


_journal_add = _ScriptMethod(304)  # AddToJournal
_journal_add.argtypes = [_str]  # Msg


def AddToJournal(Msg):
    _journal_add(Msg)


_clear_chat_ignore = _ScriptMethod(118)  # ClearChatUserIgnore


def ClearChatUserIgnore():
    _clear_chat_ignore()


_clear_journal = _ScriptMethod(119)  # ClearJournal


def ClearJournal():
    _clear_journal()


_clear_system_journal = _ScriptMethod(346)  # ClearSystemJournal


def ClearSystemJournal():
    _clear_system_journal()


_last_journal_message = _ScriptMethod(120)  # LastJournalMessage
_last_journal_message.restype = _str


def LastJournalMessage():
    return _last_journal_message()


_get_journal_line_index = _ScriptMethod(121)  # InJournal
_get_journal_line_index.restype = _int
_get_journal_line_index.argtypes = [_str]  # Str


def InJournal(Str):
    return _get_journal_line_index(Str)


_get_journal_line_index_time = _ScriptMethod(122)  # InJournalBetweenTimes
_get_journal_line_index_time.restype = _int
_get_journal_line_index_time.argtypes = [_str,  # Str
                                         _double,  # TimeBegin
                                         _double]  # TimeEnd


def InJournalBetweenTimes(Str, TimeBegin, TimeEnd):
    return _get_journal_line_index_time(Str, _pdt2ddt(TimeBegin),
                                        _pdt2ddt(TimeEnd))


_get_journal_line = _ScriptMethod(123)  # Journal
_get_journal_line.restype = _str
_get_journal_line.argtypes = [_uint]  # StringIndex


def Journal(StringIndex):
    return _get_journal_line(StringIndex)


_set_journal_line = _ScriptMethod(124)  # SetJournalLine
_set_journal_line.argtypes = [_uint,  # StringIndex
                              _str]  # Text


def SetJournalLine(StringIndex, Text):
    _set_journal_line(StringIndex, Text)


_low_journal_index = _ScriptMethod(125)  # LowJournal
_low_journal_index.restype = _int


def LowJournal():
    return _low_journal_index()


_high_journal_index = _ScriptMethod(126)  # HighJournal
_high_journal_index.restype = _int


def HighJournal():
    return _high_journal_index()


def WaitJournalLine(StartTime, Str, MaxWaitTimeMS=0):
    time = {'milliseconds': MaxWaitTimeMS} if MaxWaitTimeMS else {'weeks': 999}
    stop = StartTime + _datetime.timedelta(**time)
    while _datetime.datetime.now() <= stop:
        if InJournalBetweenTimes(Str, StartTime, stop) >= 0:
            return True
        Wait(10)
    return False


def WaitJournalLineSystem(StartTime, Str, MaxWaitTimeMS=0):
    time = {'milliseconds': MaxWaitTimeMS} if MaxWaitTimeMS else {'weeks': 999}
    stop = StartTime + _datetime.timedelta(**time)
    while _datetime.datetime.now() <= stop:
        if InJournalBetweenTimes(Str, StartTime, stop) >= 0:
            if LineName() == 'System':
                return True
        Wait(10)
    return False


_set_search_distance = _ScriptMethod(127)  # SetFindDistance
_set_search_distance.argtypes = [_uint]  # Value


def SetFindDistance(Value):
    _set_search_distance(Value)


_get_search_distance = _ScriptMethod(128)  # GetFindDistance
_get_search_distance.restype = _uint


def GetFindDistance():
    return _get_search_distance()


_set_search_vertical = _ScriptMethod(129)  # SetFindVertical
_set_search_vertical.argtypes = [_uint]  # Value


def SetFindVertical(Value):
    _set_search_vertical(Value)


_get_search_vertical = _ScriptMethod(130)  # GetFindVertical
_get_search_vertical.restype = _uint


def GetFindVertical():
    return _get_search_vertical()


_set_search_at_null = _ScriptMethod(336)  # SetFindInNulPoint
_set_search_at_null.argtypes = [_bool]  # Value


def SetFindInNulPoint(Value):
    _set_search_at_null(Value)


_get_search_at_null = _ScriptMethod(337)  # GetFindInNulPoint
_get_search_at_null.restype = _bool


def GetFindInNulPoint():
    return _get_search_at_null()


_find_graphic = _ScriptMethod(131)  # FindTypeEx
_find_graphic.restype = _uint
_find_graphic.argtypes = [_ushort,  # ObjType
                          _ushort,  # Color
                          _uint,  # Container
                          _bool]  # InSub


def FindTypeEx(ObjType, Color, Container=None, InSub=True):
    if Container is None:
        Container = Backpack()
    return _find_graphic(ObjType, Color, Container, InSub)


def FindType(ObjType, Container=None):
    if Container is None:
        Container = Backpack()
    return _find_graphic(ObjType, 0xFFFF, Container, False)


_find_graphics_array = _ScriptMethod(340)  # FindTypesArrayEx
_find_graphics_array.restype = _uint
_find_graphics_array.argtypes = [_uint,  # Len
                                 _buffer,  # ArrayBytes
                                 _uint,  # Len2
                                 _buffer,  # ArrayBytes2
                                 _uint,  # Len3
                                 _buffer,  # ArrayBytes3
                                 _bool]  # InSub


def FindTypesArrayEx(ObjTypes, Colors, Containers, InSub):
    args = []
    for array, fmt in ((ObjTypes, 'H'),
                       (Colors, 'H'),
                       (Containers, 'I')):
        args += [len(array), _struct.pack('<' + str(len(array)) + fmt, *array)]
    args.append(InSub)
    return _find_graphics_array(*args)


_find_notoriety = _ScriptMethod(132)  # FindNotoriety
_find_notoriety.restype = _uint
_find_notoriety.argtypes = [_ushort,  # ObjType
                            _ubyte]  # Notoriety


def FindNotoriety(ObjType, Notoriety):
    return _find_notoriety(ObjType, Notoriety)


_find_at_point = _ScriptMethod(133)  # FindAtCoord
_find_at_point.restype = _uint
_find_at_point.argtypes = [_ushort,  # X
                           _ushort]  # Y


def FindAtCoord(X, Y):
    return _find_at_point(X, Y)


_search_ignore = _ScriptMethod(134)  # Ignore
_search_ignore.argtypes = [_uint]  # ObjID


def Ignore(ObjID):
    _search_ignore(ObjID)


_unset_search_ignore = _ScriptMethod(135)  # IgnoreOff
_unset_search_ignore.argtypes = [_uint]  # ObjID


def IgnoreOff(ObjID):
    _unset_search_ignore(ObjID)


_reset_search_ignore = _ScriptMethod(136)  # IgnoreReset


def IgnoreReset():
    _reset_search_ignore()


_get_ignore_list = _ScriptMethod(137)  # GetIgnoreList
_get_ignore_list.restype = _buffer  # TArray


def GetIgnoreList():
    result = []
    data = _get_ignore_list()
    count = _uint.from_buffer(data)
    if count:
        fmt = '<' + count * 'I'
        result.extend(_struct.unpack(fmt, data[4:]))
    return result


_get_found_objects_list = _ScriptMethod(138)  # GetFindedList
_get_found_objects_list.restype = _buffer  # TArray


def GetFoundList():
    result = []
    data = _get_found_objects_list()
    count = _uint.from_buffer(data)
    if count:
        fmt = '<' + count * 'I'
        result.extend(_struct.unpack(fmt, data[4:]))
    return result


def GetFindedList():  # HATE THIS!!! but there is nothing to do(
    return GetFoundList()


_get_found_object = _ScriptMethod(139)  # GetFindItem
_get_found_object.restype = _uint


def FindItem():
    return _get_found_object()


_count_found_objects = _ScriptMethod(140)  # GetFindCount
_count_found_objects.restype = _int


def FindCount():
    return _count_found_objects()


_get_found_quantity = _ScriptMethod(141)  # GetFindCount
_get_found_quantity.restype = _int


def FindQuantity():
    return _get_found_quantity()


_count_found_quantities = _ScriptMethod(142)  # FindFullQuantity
_count_found_quantities.restype = _int


def FindFullQuantity():
    return _count_found_quantities()


_predicted_x = _ScriptMethod(143)  # PredictedX
_predicted_x.restype = _ushort


def PredictedX():
    return _predicted_x()


_predicted_y = _ScriptMethod(144)  # PredictedY
_predicted_y.restype = _ushort


def PredictedY():
    return _predicted_y()


_predicted_z = _ScriptMethod(145)  # PredictedZ
_predicted_z.restype = _byte


def PredictedZ():
    return _predicted_z()


_predicted_dir = _ScriptMethod(146)  # PredictedDirection
_predicted_dir.restype = _ubyte


def PredictedDirection():
    return _predicted_dir()


_get_x = _ScriptMethod(15)  # GetX
_get_x.restype = _ushort
_get_x.argtypes = [_uint]  # ObjID


def GetX(ObjID):
    return _get_x(ObjID)


_get_y = _ScriptMethod(16)  # GetY
_get_y.restype = _ushort
_get_y.argtypes = [_uint]  # ObjID


def GetY(ObjID):
    return _get_y(ObjID)


_get_z = _ScriptMethod(17)  # GetZ
_get_z.restype = _byte
_get_z.argtypes = [_uint]  # ObjID


def GetZ(ObjID):
    return _get_z(ObjID)


_get_name = _ScriptMethod(147)  # GetName
_get_name.restype = _str
_get_name.argtypes = [_uint]  # ObjectID


def GetName(ObjectID):
    return _get_name(ObjectID)


_get_alt_name = _ScriptMethod(148)  # GetAltName
_get_alt_name.restype = _str
_get_alt_name.argtypes = [_uint]  # ObjectID


def GetAltName(ObjectID):
    return _get_alt_name(ObjectID)


_get_title = _ScriptMethod(149)  # GetTitle
_get_title.restype = _str
_get_title.argtypes = [_uint]  # ObjID


def GetTitle(ObjID):
    return _get_title(ObjID)


_get_tooltip = _ScriptMethod(150)  # GetTooltip
_get_tooltip.restype = _str
_get_tooltip.argtypes = [_uint]  # ObjID


def GetTooltip(ObjID):
    return _get_tooltip(ObjID)


def GetCliloc(ObjID):
    return GetTooltip(ObjID)


_get_graphic = _ScriptMethod(151)  # GetType
_get_graphic.restype = _ushort
_get_graphic.argtypes = [_uint]  # ObjID


def GetType(ObjID):
    return _get_graphic(ObjID)


_get_tooltip_obj = _ScriptMethod(152)  # GetToolTipRec
_get_tooltip_obj.restype = _buffer  # Array of TClilocRec
_get_tooltip_obj.argtypes = [_uint]  # ObjID


def GetTooltipRec(ObjID):
    result = []
    data = _get_tooltip_obj(ObjID)
    count = _uint.from_buffer(data)
    offset = 4
    for i in range(count):
        cliloc, length = _struct.unpack_from('<iI', data, offset)
        offset += 8
        strings = []
        for j in range(length):
            string = _str.from_buffer(data, offset)
            offset += _struct.calcsize(string.fmt)
            strings.append(string.value)
        result.append({'Cliloc_ID': cliloc, 'Params': strings})
    return result


_get_object_tooltip = _ScriptMethod(153)  # GetClilocByID
_get_object_tooltip.restype = _str
_get_object_tooltip.argtypes = [_uint]  # ClilocID


def GetClilocByID(ClilocID):
    return _get_object_tooltip(ClilocID)


_get_quantity = _ScriptMethod(154)  # GetQuantity
_get_quantity.restype = _int
_get_quantity.argtypes = [_uint]  # ObjID


def GetQuantity(ObjID):
    return _get_quantity(ObjID)


_is_object_exists = _ScriptMethod(155)  # IsObjectExists
_is_object_exists.restype = _bool
_is_object_exists.argtypes = [_uint]  # ObjID


def IsObjectExists(ObjID):
    return _is_object_exists(ObjID)


_is_npc = _ScriptMethod(172)  # IsNPC
_is_npc.restype = _bool
_is_npc.argtypes = [_uint]  # ObjID


def IsNPC(ObjID):
    return _is_npc(ObjID)


_get_price = _ScriptMethod(156)  # GetPrice
_get_price.restype = _uint
_get_price.argtypes = [_uint]  # ObjID


def GetPrice(ObjID):
    return _get_price(ObjID)


_get_direction = _ScriptMethod(157)  # GetDirection
_get_direction.restype = _ubyte
_get_direction.argtypes = [_uint]  # ObjID


def GetDirection(ObjID):
    return _get_direction(ObjID)


_get_distance = _ScriptMethod(158)  # GetDistance
_get_distance.restype = _int
_get_distance.argtypes = [_uint]  # ObjID


def GetDistance(ObjID):
    return _get_distance(ObjID)


_get_color = _ScriptMethod(159)  # GetColor
_get_color.restype = _ushort
_get_color.argtypes = [_uint]  # ObjID


def GetColor(ObjID):
    return _get_color(ObjID)


_get_strength = _ScriptMethod(160)  # GetStr
_get_strength.restype = _int
_get_strength.argtypes = [_uint]  # ObjID


def GetStr(ObjID):
    return _get_strength(ObjID)


_get_intelligence = _ScriptMethod(161)  # GetInt
_get_intelligence.restype = _int
_get_intelligence.argtypes = [_uint]  # ObjID


def GetInt(ObjID):
    return _get_intelligence(ObjID)


_get_dexterity = _ScriptMethod(162)  # GetDex
_get_dexterity.restype = _int
_get_dexterity.argtypes = [_uint]  # ObjID


def GetDex(ObjID):
    return _get_dexterity(ObjID)


_get_hp = _ScriptMethod(163)  # GetHP
_get_hp.restype = _int
_get_hp.argtypes = [_uint]  # ObjID


def GetHP(ObjID):
    result = _get_hp(ObjID)
    if not result and _is_object_exists(ObjID) and _is_npc(ObjID):
        _request_stats(ObjID)
        Wait(100)
        result = _get_hp(ObjID)
    return result


_get_max_hp = _ScriptMethod(164)  # GetMaxHP
_get_max_hp.restype = _int
_get_max_hp.argtypes = [_uint]  # ObjID


def GetMaxHP(ObjID):
    return _get_max_hp(ObjID)


_get_mana = _ScriptMethod(165)  # GetMana
_get_mana.restype = _int
_get_mana.argtypes = [_uint]  # ObjID


def GetMana(ObjID):
    result = _get_mana(ObjID)
    if not result and _is_object_exists(ObjID) and _is_npc(ObjID):
        _request_stats(ObjID)
        Wait(100)
        result = _get_mana(ObjID)
    return result


_get_max_mana = _ScriptMethod(166)  # GetMaxMana
_get_max_mana.restype = _int
_get_max_mana.argtypes = [_uint]  # ObjID


def GetMaxMana(ObjID):
    return _get_max_mana(ObjID)


_get_stamina = _ScriptMethod(167)  # GetStam
_get_stamina.restype = _int
_get_stamina.argtypes = [_uint]  # ObjID


def GetStam(ObjID):
    result = _get_stamina(ObjID)
    if not result and _is_object_exists(ObjID) and _is_npc(ObjID):
        _request_stats(ObjID)
        Wait(100)
        result = _get_stamina(ObjID)
    return result


_get_max_stamina = _ScriptMethod(168)  # GetMaxStam
_get_max_stamina.restype = _int
_get_max_stamina.argtypes = [_uint]  # ObjID


def GetMaxStam(ObjID):
    return _get_max_stamina(ObjID)


_get_notoriety = _ScriptMethod(169)  # GetNotoriety
_get_notoriety.restype = _ubyte
_get_notoriety.argtypes = [_uint]  # ObjId


def GetNotoriety(ObjID):
    return _get_notoriety(ObjID)


_get_container = _ScriptMethod(170)  # GetParent
_get_container.restype = _uint
_get_container.argtypes = [_uint]  # ObjID


def GetParent(ObjID):
    return _get_container(ObjID)


def IsWarMode(ObjID):
    return _get_warmode(ObjID)


_get_dead_status = _ScriptMethod(173)  # IsDead
_get_dead_status.restype = _bool
_get_dead_status.argtypes = [_uint]  # ObjID


def IsDead(ObjID):
    return _get_dead_status(ObjID)


_get_running_status = _ScriptMethod(174)  # IsRunning
_get_running_status.restype = _bool
_get_running_status.argtypes = [_uint]  # ObjID


def IsRunning(ObjID):
    return _get_running_status(ObjID)


_is_container = _ScriptMethod(175)  # IsContainer
_is_container.restype = _bool
_is_container.argtypes = [_uint]  # ObjID


def IsContainer(ObjID):
    return _is_container(ObjID)


_get_hidden_status = _ScriptMethod(176)  # IsHidden
_get_hidden_status.restype = _bool
_get_hidden_status.argtypes = [_uint]  # ObjID


def IsHidden(ObjID):
    return _get_hidden_status(ObjID)


_is_movable = _ScriptMethod(177)  # IsMovable
_is_movable.restype = _bool
_is_movable.argtypes = [_uint]  # ObjID


def IsMovable(ObjID):
    return _is_movable(ObjID)


_get_yellow_hits_status = _ScriptMethod(178)  # IsYellowHits
_get_yellow_hits_status.restype = _bool
_get_yellow_hits_status.argtypes = [_uint]  # ObjID


def IsYellowHits(ObjID):
    return _get_yellow_hits_status(ObjID)


_get_poisoned_status = _ScriptMethod(179)  # IsPoisoned
_get_poisoned_status.restype = _bool
_get_poisoned_status.argtypes = [_uint]  #


def IsPoisoned(ObjID):
    return _get_poisoned_status(ObjID)


_get_paralyzed_status = _ScriptMethod(180)  # IsParalyzed
_get_paralyzed_status.restype = _bool
_get_paralyzed_status.argtypes = [_uint]  # ObjID


def IsParalyzed(ObjID):
    return _get_paralyzed_status(ObjID)


_is_female = _ScriptMethod(181)  # IsFemale
_is_female.restype = _bool
_is_female.argtypes = [_uint]  # ObjID


def IsFemale(ObjID):
    return _is_female(ObjID)


_open_door = _ScriptMethod(182)  # OpenDoor


def OpenDoor():
    _open_door()


_bow = _ScriptMethod(183)  # Bow


def Bow():
    _bow()


_salute = _ScriptMethod(184)  # Salute


def Salute():
    _salute()


_get_picked_item = _ScriptMethod(185)  # GetPickupedItem
_get_picked_item.restype = _uint


def GetPickupedItem():
    return _get_picked_item()


_set_picked_item = _ScriptMethod(186)  # SetPickupedItem
_set_picked_item.argtypes = [_uint]  # ID


def SetPickupedItem(ID):
    _set_picked_item(ID)


_get_drop_check_coord = _ScriptMethod(187)  # GetDropCheckCoord
_get_drop_check_coord.restype = _bool


def GetDropCheckCoord():
    return _get_drop_check_coord()


_set_drop_check_coord = _ScriptMethod(188)  # SetDropCheckCoord
_set_drop_check_coord.argtypes = [_bool]  # Value


def SetDropCheckCoord(Value):
    _set_drop_check_coord(Value)


_get_drop_delay = _ScriptMethod(189)  # GetDropDelay
_get_drop_delay.restype = _uint


def GetDropDelay():
    return _get_drop_delay()


_set_drop_delay = _ScriptMethod(190)  # SetDropDelay
_set_drop_delay.argtypes = [_uint]  # Value


def SetDropDelay(Value):
    _set_drop_delay(Value)


_drag_item = _ScriptMethod(191)  # DragItem
_drag_item.restype = _bool
_drag_item.argtypes = [_uint,  # ItemID
                       _int]  # Count


def DragItem(ItemID, Count):
    return _drag_item(ItemID, Count)


_drop_item = _ScriptMethod(192)  # DropItem
_drop_item.restype = _bool
_drop_item.argtypes = [_uint,  # MoveIntoID
                       _int,  # X
                       _int,  # Y
                       _int]  # Z


def DropItem(MoveIntoID, X, Y, Z):
    return _drop_item(MoveIntoID, X, Y, Z)


def MoveItem(ItemID, Count, MoveIntoID, X, Y, Z):
    if not DragItem(ItemID, Count):
        return False
    Wait(100)
    return DropItem(MoveIntoID, X, Y, Z)


def Grab(ItemID, Count):
    return MoveItem(ItemID, Count, Backpack(), 0, 0, 0)


def Drop(ItemID, Count, X, Y, Z):
    return MoveItem(ItemID, Count, Ground(), X, Y, Z)


def DropHere(ItemID):
    return MoveItem(ItemID, 0, Ground(), 0, 0, 0)


def MoveItems(Container, ItemsType, ItemsColor, MoveIntoID, X, Y, Z,
              DelayMS, MaxCount=0):
    FindTypeEx(ItemsType, ItemsColor, Container, False)
    items = GetFoundList()
    if not items:  # nothing found
        return False
    drop_delay = GetDropDelay()
    if not 50 <= drop_delay <= 10000:
        drop_delay = 50 if drop_delay < 50 else 10000
    if drop_delay > DelayMS:
        DelayMS = 0
    SetDropDelay(drop_delay)
    if not 0 < MaxCount < len(items):
        MaxCount = len(items)
    for i in range(MaxCount):
        MoveItem(items[i], 0, MoveIntoID, X, Y, Z)
        Wait(DelayMS)
    return True


def EmptyContainer(Container, DestContainer, delay_ms):
    return MoveItems(Container, -1, -1, DestContainer,
                     0xFFFF, 0xFFFF, 0, delay_ms)


_request_context_menu = _ScriptMethod(193)  # RequestContextMenu
_request_context_menu.argtypes = [_uint]  # ID


def RequestContextMenu(ID):
    _request_context_menu(ID)


_wait_context_menu = _ScriptMethod(194)  # SetContextMenuHook
_wait_context_menu.argtypes = [_uint,  # MenuID
                               _ubyte]  # EntryNumber


def SetContextMenuHook(MenuID, EntryNumber):
    _wait_context_menu(MenuID, EntryNumber)


_get_context_menu = _ScriptMethod(195)  # GetContextMenu
_get_context_menu.restype = _buffer


def GetContextMenu():
    result = []
    data = _get_context_menu()
    count = _uint.from_buffer(data)
    offset = count.size
    while 42:
        if offset >= len(data) - 1:
            break
        string = _str.from_buffer(data, offset)
        offset += string.size
        result.append(string.value)
    return result


_get_context_menu_record = _ScriptMethod(345)  # GetContextMenuRec
_get_context_menu_record.restype = _buffer  # TODO: What is this do?


def GetContextMenuRec():
    """
    fmt = 'HH'
    data = _get_context_menu_record()
    keys = 'Tag', 'Flags'
    serial, count, tmp = _struct.unpack('>IBI', data[:9])
    l = []
    for i in range(count):
        l.append(_struct.unpack('HHIHH', data[9+i*12:9+i*12+12]))
    """
    return None


_clear_context_menu = _ScriptMethod(196)  # ClearContextMenu


def ClearContextMenu():
    _clear_context_menu()


_is_trade = _ScriptMethod(197)  # CheckTradeState
_is_trade.restype = _bool


def IsTrade():
    return _is_trade()


_get_trade_container_serial = _ScriptMethod(198)  # GetTradeContainer
_get_trade_container_serial.restype = _uint
_get_trade_container_serial.argtypes = [_ubyte,  # TradeNum
                                        _ubyte]  # Num


def GetTradeContainer(TradeNum, Num):
    return _get_trade_container_serial(TradeNum, Num)


_get_trade_opponent_serial = _ScriptMethod(199)  # GetTradeOpponent
_get_trade_opponent_serial.restype = _uint
_get_trade_opponent_serial.argtypes = [_ubyte]  # TradeNum


def GetTradeOpponent(TradeNum):
    return _get_trade_opponent_serial(TradeNum)


_get_trades_count = _ScriptMethod(200)  # GetTradeCount
_get_trades_count.restype = _ubyte


def TradeCount():
    return _get_trades_count()


_get_trade_opponent_name = _ScriptMethod(201)  # GetTradeOpponentName
_get_trade_opponent_name.restype = _str
_get_trade_opponent_name.argtypes = [_ubyte]  # TradeNum


def GetTradeOpponentName(TradeNum):
    return _get_trade_opponent_name(TradeNum)


_get_trade_state = _ScriptMethod(202)  # TradeCheck
_get_trade_state.restype = _bool
_get_trade_state.argtypes = [_ubyte,  # TradeNum
                             _ubyte]  # Num


def TradeCheck(TradeNum, Num):
    return _get_trade_state(TradeNum, Num)


_confirm_trade = _ScriptMethod(203)  # ConfirmTrade
_confirm_trade.argtypes = [_ubyte]  # TradeNum


def ConfirmTrade(TradeNum):
    _confirm_trade(TradeNum)


_cancel_trade = _ScriptMethod(204)  # CancelTrade
_cancel_trade.restype = _bool
_cancel_trade.argtypes = [_ubyte]  # TradeNum


def CancelTrade(TradeNum):
    return _cancel_trade(TradeNum)


_wait_menu = _ScriptMethod(205)  # WaitMenu
_wait_menu.argtypes = [_str,  # MenuCaption
                       _str]  # ElementCaption


def WaitMenu(MenuCaption, ElementCaption):
    _wait_menu(MenuCaption, ElementCaption)


_auto_menu = _ScriptMethod(206)  # AutoMenu
_auto_menu.argtypes = [_str,  # MenuCaption
                       _str]  # ElementCaption


def AutoMenu(MenuCaption, ElementCaption):
    _auto_menu(MenuCaption, ElementCaption)


_is_menu_hook = _ScriptMethod(207)  # MenuHookPresent
_is_menu_hook.restype = _bool


def MenuHookPresent():
    return _is_menu_hook()


_is_menu = _ScriptMethod(208)  # MenuPresent
_is_menu.restype = _bool


def MenuPresent():
    return _is_menu()


_cancel_menu = _ScriptMethod(209)  # CancelMenu


def CancelMenu():
    _cancel_menu()


def CancelAllMenuHooks():
    _cancel_menu()


_close_menu = _ScriptMethod(210)  # CloseMenu


def CloseMenu():
    _close_menu()


_get_menu = _ScriptMethod(338)  # GetMenuItems
_get_menu.restype = _buffer
_get_menu.argtypes = [_str]  # MenuCaption


def GetMenu(MenuCaption):
    result = []
    data = _get_menu(MenuCaption)
    count = _uint.from_buffer(data)
    offset = count.size
    while 42:
        if offset >= len(data) - 1:
            break
        string = _str.from_buffer(data, offset)
        result.append(string.value)
        offset += string.size
    return result


def GetMenuItems(MenuCaption):
    return '\n'.join(GetMenu(MenuCaption))


_get_last_menu = _ScriptMethod(339)  # GetLastMenuItems
_get_last_menu.restype = _buffer


def GetLastMenu():
    result = []
    data = _get_last_menu()
    count = _uint.from_buffer(data)
    offset = count.size
    while 42:
        if offset >= len(data) - 1:
            break
        string = _str.from_buffer(data, offset)
        result.append(string.value)
        offset += string.size
    return result


def GetLastMenuItems():
    return '\n'.join(GetLastMenu())


_wait_gump = _ScriptMethod(211)  # WaitGumpInt
_wait_gump.argtypes = [_int]  # Value


def WaitGump(Value):
    _wait_gump(int(Value))


_wait_gump_text_entry = _ScriptMethod(212)  # WaitGumpTextEntry
_wait_gump_text_entry.argtypes = [_str]  # Value


def WaitTextEntry(Value):
    _wait_gump_text_entry(Value)


_auto_text_entry = _ScriptMethod(213)  # GumpAutoTextEntry
_auto_text_entry.argtypes = [_int,  # TextEntryID
                             _str]  # Value


def GumpAutoTextEntry(TextEntryID, Value):
    _auto_text_entry(TextEntryID, Value)


_auto_radiobutton = _ScriptMethod(214)  # GumpAutoRadiobutton
_auto_radiobutton.argtypes = [_int,  # RadiobuttonID
                              _int]  # Value


def GumpAutoRadiobutton(RadiobuttonID, Value):
    _auto_radiobutton(RadiobuttonID, Value)


_auto_checkbox = _ScriptMethod(215)  # GumpAutoCheckBox
_auto_checkbox.argtypes = [_int,  # CBID
                           _int]  # Value


def GumpAutoCheckBox(CBID, Value):
    _auto_checkbox(CBID, Value)


_send_gump_button = _ScriptMethod(216)  # NumGumpButton
_send_gump_button.restype = _bool
_send_gump_button.argtypes = [_ushort,  # GumpIndex
                              _int]  # Value


def NumGumpButton(GumpIndex, Value):
    return _send_gump_button(GumpIndex, Value)


_send_gump_text_entry = _ScriptMethod(217)  # NumGumpTextEntry
_send_gump_text_entry.restype = _bool
_send_gump_text_entry.argtypes = [_ushort,  # GumpIndex
                                  _int,  # TextEntryID
                                  _str]  # Value


def NumGumpTextEntry(GumpIndex, TextEntryID, Value):
    return _send_gump_text_entry(GumpIndex, TextEntryID, Value)


_send_gump_radiobutton = _ScriptMethod(218)  # NumGumpRadiobutton
_send_gump_radiobutton.restype = _bool
_send_gump_radiobutton.argtypes = [_ushort,  # GumpIndex
                                   _int,  # RadiobuttonID
                                   _int]  # Value


def NumGumpRadiobutton(GumpIndex, RadiobuttonID, Value):
    return _send_gump_radiobutton(GumpIndex, RadiobuttonID, Value)


_send_gump_checkbox = _ScriptMethod(219)  # NumGumpCheckBox
_send_gump_checkbox.restype = _bool
_send_gump_checkbox.argtypes = [_ushort,  # GumpIndex
                                _int,  # CBID
                                _int]  # Value


def NumGumpCheckBox(GumpIndex, CBID, Value):
    return _send_gump_checkbox(GumpIndex, CBID, Value)


_get_gumps_count = _ScriptMethod(220)  # GetGumpsCount
_get_gumps_count.restype = _ushort


def GetGumpsCount():
    return _get_gumps_count()


_close_gump = _ScriptMethod(221)  # CloseSimpleGump
_close_gump.argtypes = [_ushort]  # GumpIndex


def CloseSimpleGump(GumpIndex):
    _close_gump(GumpIndex)


def IsGump():
    return GetGumpsCount() > 0


_get_gump_serial = _ScriptMethod(222)  # GetGumpSerial
_get_gump_serial.restype = _uint
_get_gump_serial.argtypes = [_ushort]  # GumpIndex


def GetGumpSerial(GumpIndex):
    return _get_gump_serial(GumpIndex)


_get_gump_type = _ScriptMethod(223)  # GetGumpID
_get_gump_type.restype = _uint
_get_gump_type.argtypes = [_ushort]  # GumpIndex


def GetGumpID(GumpIndex):
    return _get_gump_type(GumpIndex)


_get_gump_no_close = _ScriptMethod(224)  # GetGumpNoClose
_get_gump_no_close.restype = _bool
_get_gump_no_close.argtypes = [_ushort]  # GumpIndex


def IsGumpCanBeClosed(GumpIndex):
    return _get_gump_no_close(GumpIndex)


_get_gump_text = _ScriptMethod(225)  # GetGumpTextLines
_get_gump_text.restype = _buffer
_get_gump_text.argtypes = [_ushort]  # GumpIndex


def GetGumpTextLines(GumpIndex):
    result = []
    data = _get_gump_text(GumpIndex)
    count = _uint.from_buffer(data)
    offset = count.size
    while 42:
        if offset >= len(data) - 1:
            break
        string = _str.from_buffer(data, offset)
        offset += string.size
        result.append(string.value)
    return result


_get_gump_full_lines = _ScriptMethod(226)  # GetGumpFullLines
_get_gump_full_lines.restype = _buffer
_get_gump_full_lines.argtypes = [_ushort]  # GumpIndex


def GetGumpFullLines(GumpIndex):
    result = []
    data = _get_gump_full_lines(GumpIndex)
    count = _uint.from_buffer(data)
    offset = count.size
    while 42:
        if offset >= len(data) - 1:
            break
        string = _str.from_buffer(data, offset)
        offset += string.size
        result.append(string.value)
    return result


_get_gump_short_lines = _ScriptMethod(227)  # GetGumpShortLines
_get_gump_short_lines.restype = _buffer
_get_gump_short_lines.argtypes = [_ushort]  # GumpIndex


def GetGumpShortLines(GumpIndex):
    result = []
    data = _get_gump_short_lines(GumpIndex)
    count = _uint.from_buffer(data)
    offset = count.size
    while 42:
        if offset >= len(data) - 1:
            break
        string = _str.from_buffer(data, offset)
        offset += string.size
        result.append(string.value)
    return result


_get_gump_buttons = _ScriptMethod(228)  # GetGumpButtonsDescription
_get_gump_buttons.restype = _buffer
_get_gump_buttons.argtypes = [_ushort]  # GumpIndex


def GetGumpButtonsDescription(GumpIndex):
    result = []
    data = _get_gump_buttons(GumpIndex)
    count = _uint.from_buffer(data)
    offset = count.size
    while 42:
        if offset >= len(data) - 1:
            break
        string = _str.from_buffer(data, offset)
        offset += string.size
        result.append(string.value)
    return result


_get_gump_info = _ScriptMethod(229)  # GetGumpInfo
_get_gump_info.restype = _buffer  # TGumpInfo
_get_gump_info.argtypes = [_ushort]  # GumpIndex


class _Group:
    args = [_int] * 3
    container = 'groups'
    keys = 'GroupNumber', 'Page', 'ElemNum'


class _EndGroup(_Group):
    container = 'EndGroups'


class _GumpButton:
    args = [_int] * 9
    container = 'GumpButtons'
    keys = ('X', 'Y', 'ReleasedID', 'PressedID', 'Quit', 'PageID',
            'ReturnValue', 'Page', 'ElemNum')


class _ButtonTileArt:
    args = [_int] * 12
    container = 'ButtonTileArts'
    keys = ('X', 'Y', 'ReleasedID', 'PressedID', 'Quit', 'PageID',
            'ReturnValue', 'ArtID', 'Hue', 'ArtX', 'ArtY', 'ElemNum')


class _CheckBox:
    args = [_int] * 8
    container = 'CheckBoxes'
    keys = ('X', 'Y', 'ReleasedID', 'PressedID', 'Status', 'ReturnValue',
            'Page', 'ElemNum')


class _ChekerTrans:
    args = [_int] * 6
    container = 'ChekerTrans'
    keys = 'X', 'Y', 'Width', 'Height', 'Page', 'ElemNum'


class _CroppedText:
    args = [_int] * 8
    container = 'CroppedText'
    keys = 'X', 'Y', 'Width', 'Height', 'Color', 'TextID', 'Page', 'ElemNum'


class _GumpPic:
    args = [_int] * 6
    container = 'GumpPics'
    keys = 'X', 'Y', 'ID', 'Hue', 'Page', 'ElemNum'


class _GumpPicTiled:
    fmt = '=7i'
    args = [_int] * 7
    container = 'GumpPicTiled'
    keys = 'X', 'Y', 'Width', 'Height', 'GumpID', 'Page', 'ElemNum'


class _Radiobutton:
    args = [_int] * 8
    container = 'RadioButtons'
    keys = ('X', 'Y', 'ReleasedID', 'PressedID', 'Status', 'ReturnValue',
            'Page', 'ElemNum')


class _ResizePic:
    args = [_int] * 7
    container = 'ResizePics'
    keys = 'X', 'Y', 'GumpID', 'Width', 'Height', 'Page', 'ElemNum'


class _GumpText:
    args = [_int] * 6
    container = 'GumpText'
    keys = 'X', 'Y', 'Color', 'TextID', 'Page', 'ElemNum'


class _TextEntry:
    args = [_int] * 7 + [_str, _int, _int]
    container = 'TextEntries'
    keys = ('X', 'Y', 'Width', 'Height', 'Color', 'ReturnValue',
            'DefaultTextID', 'RealValue', 'Page', 'ElemNum')


class _Text:
    args = [_str]
    container = 'Text'
    keys = None


class _TextEntryLimited:
    args = [_int] * 10
    container = 'TextEntriesLimited'
    keys = ('X', 'Y', 'Width', 'Height', 'Color', 'ReturnValue',
            'DefaultTextID', 'Limit', 'Page', 'ElemNum')


class _TilePic:
    args = [_int] * 5
    container = 'TilePics'
    keys = 'X', 'Y', 'ID', 'Page', 'ElemNum'


class _TilePicHue:
    args = [_int] * 6
    container = 'TilePicHue'
    keys = 'X', 'Y', 'ID', 'Color', 'Page', 'ElemNum'


class _Tooltip:
    args = [_uint, _str, _int, _int]
    container = 'Tooltips'
    keys = 'ClilocID', 'Arguments', 'Page', 'ElemNum'


class _HtmlGump:
    args = [_int] * 9
    container = 'HtmlGump'
    keys = ('X', 'Y', 'Width', 'Height', 'TextID', 'Background', 'Scrollbar',
            'Page', 'ElemNum')


class _XmfHtmlGump:
    args = [_int] * 4 + [_uint] + [_int] * 4
    container = 'XmfHtmlGump'
    keys = ('X', 'Y', 'Width', 'Height', 'ClilocID', 'Background', 'Scrollbar',
            'Page', 'ElemNum')


class _XmfHTMLGumpColor:
    args = [_int] * 4 + [_uint] + [_int] * 5
    container = 'XmfHTMLGumpColor'
    keys = ('X', 'Y', 'Width', 'Height', 'ClilocID', 'Background', 'Scrollbar',
            'Hue', 'Page', 'ElemNum')


class _XmfHTMLTok:
    args = [_int] * 7 + [_uint, _str, _int, _int]
    container = 'XmfHTMLTok'
    keys = ('X', 'Y', 'Width', 'Height', 'Background', 'Scrollbar', 'Color',
            'ClilocID', 'Arguments', 'Page', 'ElemNum')


class _ItemProperty:
    args = [_uint, _int]
    container = 'ItemProperties'
    keys = 'Prop', 'ElemNum'


class _Gump:
    fmt = '<2I2hi4?'
    args = [_uint, _uint, _short, _short, _int] + [_bool] * 4
    keys = ('Serial', 'GumpID', 'X', 'Y', 'Pages', 'NoMove', 'NoResize',
            'NoDispose', 'NoClose')


def GetGumpInfo(GumpIndex):
    data = _get_gump_info(GumpIndex)
    values = _struct.unpack_from(_Gump.fmt, data, 0)
    result = dict(zip(_Gump.keys, values))
    offset = _struct.calcsize(_Gump.fmt)
    # parse elements
    elements = (_Group, _EndGroup, _GumpButton, _ButtonTileArt, _CheckBox,
                _ChekerTrans, _CroppedText, _GumpPic, _GumpPicTiled,
                _Radiobutton, _ResizePic, _GumpText, _TextEntry, _Text,
                _TextEntryLimited, _TilePic, _TilePicHue, _Tooltip,
                _HtmlGump, _XmfHtmlGump, _XmfHTMLGumpColor, _XmfHTMLTok,
                _ItemProperty)
    for cls in elements:
        result[cls.container] = []
        count = _uint.from_buffer(data, offset)
        offset += count.size
        for i in range(count):
            values = []
            for arg in cls.args:
                element = arg.from_buffer(data, offset)
                offset += element.size
                values.append(element.value)
            if cls is _Text:
                result[cls.container].append(
                    *[values])  # there is only one element
            else:
                element = dict(zip(cls.keys, values))
                if 'ClilocID' in cls.keys and 'Arguments' in cls.keys:  # need to represent clilocs
                    text = GetClilocByID(element['ClilocID'])
                    args = element.get('Arguments', '')
                    args = args.split('@')[1:] or []
                    for arg in args:
                        if '~' in text:
                            if arg.startswith('#'):  # another cliloc
                                arg = GetClilocByID(int(arg.strip('#')))
                            s = text.index('~')
                            e = text.index('~', s + 1)
                            text = text.replace(text[s:e + 1], arg,
                                                1) or arg  # TODO: wtf?
                    element['Arguments'] = text
                result[cls.container].append(element)
    return result


_ignore_gump_id = _ScriptMethod(230)  # AddGumpIgnoreByID
_ignore_gump_id.argtypes = [_uint]  # ID


def AddGumpIgnoreByID(ID):
    _ignore_gump_id(ID)


_ignore_gump_serial = _ScriptMethod(231)  # AddGumpIgnoreBySerial
_ignore_gump_serial.argtypes = [_uint]  # Serial


def AddGumpIgnoreBySerial(Serial):
    _ignore_gump_serial(Serial)


_gumps_ignore_reset = _ScriptMethod(232)  # ClearGumpsIgnore


def ClearGumpsIgnore():
    _gumps_ignore_reset()


def RhandLayer():
    return 0x01


def LhandLayer():
    return 0x02


def ShoesLayer():
    return 0x03


def PantsLayer():
    return 0x04


def ShirtLayer():
    return 0x05


def HatLayer():
    return 0x06


def GlovesLayer():
    return 0x07


def RingLayer():
    return 0x08


def TalismanLayer():
    return 0x09


def NeckLayer():
    return 0x0A


def HairLayer():
    return 0x0B


def WaistLayer():
    return 0x0C


def TorsoLayer():
    return 0x0D


def BraceLayer():
    return 0x0E


def BeardLayer():
    return 0x10


def TorsoHLayer():
    return 0x11


def EarLayer():
    return 0x12


def ArmsLayer():
    return 0x13


def CloakLayer():
    return 0x14


def BpackLayer():
    return 0x15


def RobeLayer():
    return 0x16


def EggsLayer():
    return 0x17


def LegsLayer():
    return 0x18


def HorseLayer():
    return 0x19


def RstkLayer():
    return 0x1A


def NRstkLayer():
    return 0x1B


def SellLayer():
    return 0x1C


def BankLayer():
    return 0x1D


_get_obj_at_layer = _ScriptMethod(233)  # ObjAtLayerEx
_get_obj_at_layer.restype = _uint
_get_obj_at_layer.argtypes = [_ubyte,  # LayerType
                              _uint]  # PlayerID


def ObjAtLayerEx(LayerType, PlayerID):
    return _get_obj_at_layer(LayerType, PlayerID)


def ObjAtLayer(LayerType):
    return ObjAtLayerEx(LayerType, Self())


_get_layer = _ScriptMethod(234)  # GetLayer
_get_layer.restype = _ubyte
_get_layer.argtypes = [_uint]  # Obj


def GetLayer(Obj):
    return _get_layer(Obj)


_wear_item = _ScriptMethod(235)  # WearItem
_wear_item.argtypes = [_ubyte,  # Layer
                       _uint]  # Obj


def WearItem(Layer, Obj):
    if GetPickupedItem() == 0 or Layer == 0 or Self() == 0:
        return False
    _wear_item(Layer, Obj)
    SetPickupedItem(0)
    return True


def Disarm():
    backpack = Backpack()
    tmp = []
    for layer in LhandLayer(), RhandLayer():
        item = ObjAtLayer(layer)
        if item:
            tmp.append(MoveItem(item, 1, backpack, 0, 0, 0))
    return all(tmp)


def disarm():
    return Disarm()


def Equip(Layer, Obj):
    if Layer and DragItem(Obj, 1):
        return WearItem(Layer, Obj)
    return False


def equip(Layer, Obj):
    return Equip(Layer, Obj)


def Equipt(Layer, ObjType):
    item = FindType(ObjType, Backpack())
    if item:
        return Equip(Layer, item)
    return False


def equipt(Layer, ObjType):
    return Equipt(Layer, ObjType)


def UnEquip(Layer):
    item = ObjAtLayer(Layer)
    if item:
        return MoveItem(item, 1, Backpack(), 0, 0, 0)
    return False


_get_dress_delay = _ScriptMethod(236)  # GetDressSpeed
_get_dress_delay.restype = _ushort


def GetDressSpeed():
    return _get_dress_delay()


_set_dress_delay = _ScriptMethod(237)  # SetDressSpeed
_set_dress_delay.argtypes = [_ushort]  # Value


def SetDressSpeed(Value):
    _set_dress_delay(Value)


_get_client_version_int = _ScriptMethod(355)  # SCGetClientVersionInt
_get_client_version_int.restype = _int


def GetClientVersionInt():
    return _get_client_version_int()


_wearable_layers = (RhandLayer(), LhandLayer(), ShoesLayer(), PantsLayer(),
                    ShirtLayer(), HatLayer(), GlovesLayer(), RingLayer(),
                    NeckLayer(), WaistLayer(), TorsoLayer(), BraceLayer(),
                    TorsoHLayer(), EarLayer(), ArmsLayer(), CloakLayer(),
                    RobeLayer(), EggsLayer(), LegsLayer())

_unequip_itemsset_macro = _ScriptMethod(356)  # SCUnequipItemsSetMacro


def UnequipItemsSetMacro():
    _unequip_itemsset_macro()


def Undress():
    tmp = []
    client_version_int = GetClientVersionInt()
    if client_version_int < 7007400:
        delay = GetDressSpeed()
        char = Self()
        backpack = Backpack()
        for layer in _wearable_layers:
            item = ObjAtLayerEx(layer, char)
            if item:
                tmp.append(MoveItem(item, 1, backpack, 0, 0, 0))
                Wait(delay)
    else:
        UnequipItemsSetMacro()
        tmp.append(True)
    # no need to wait - all this done inside
    return all(tmp)


_set_dress = _ScriptMethod(238)  # SetDress


def SetDress():
    _set_dress()


_equip_item_set_macro = _ScriptMethod(357)  # SCEquipItemsSetMacro


def EquipItemsSetMacro():
    _equip_item_set_macro()


_get_dress_set = _ScriptMethod(239)  # GetDressSet
_get_dress_set.restype = _buffer  # TLayersObjectsList


def EquipDressSet():
    res = []
    client_version_int = GetClientVersionInt()
    if client_version_int < 7007400:
        delay = GetDressSpeed()
        data = _get_dress_set()
        count = _uint.from_buffer(data)
        data = data[count.size:]
        offset = 0
        for i in range(count):
            layer, item = _struct.unpack_from('<BI', data, offset)
            offset += 5
            if item:
                res.append(Equip(layer, item))
                Wait(delay)
    else:
        EquipItemsSetMacro()
        res.append(True)
    # no need to wait - all this done inside
    return all(res)


def DressSavedSet():
    EquipDressSet()


def Count(ObjType):
    FindType(ObjType, Backpack())
    return FindFullQuantity()


def CountGround(ObjType):
    FindType(ObjType, Ground())
    return FindFullQuantity()


def CountEx(ObjType, Color, Container):
    FindTypeEx(ObjType, Color, Container, False)
    return FindFullQuantity()


def BP(): return 0X0F7A


def BM(): return 0x0F7B


def GA(): return 0x0F84


def GS(): return 0x0F85


def MR(): return 0x0F86


def NS(): return 0x0F88


def SA(): return 0x0F8C


def SS(): return 0x0F8D


def BPCount():
    FindTypeEx(BP(), 0, Backpack(), True)
    return FindFullQuantity()


def BMCount():
    FindTypeEx(BM(), 0, Backpack(), True)
    return FindFullQuantity()


def GACount():
    FindTypeEx(GA(), 0, Backpack(), True)
    return FindFullQuantity()


def GSCount():
    FindTypeEx(GS(), 0, Backpack(), True)
    return FindFullQuantity()


def MRCount():
    FindTypeEx(MR(), 0, Backpack(), True)
    return FindFullQuantity()


def NSCount():
    FindTypeEx(NS(), 0, Backpack(), True)
    return FindFullQuantity()


def SACount():
    FindTypeEx(SA(), 0, Backpack(), True)
    return FindFullQuantity()


def SSCount():
    FindTypeEx(SS(), 0, Backpack(), True)
    return FindFullQuantity()


_auto_buy = _ScriptMethod(240)  # AutoBuy
_auto_buy.argtypes = [_ushort,  # ItemType
                      _ushort,  # ItemColor
                      _ushort]  # Quantity


def AutoBuy(ItemType, ItemColor, Quantity):
    _auto_buy(ItemType, ItemColor, Quantity)


_get_shop_list = _ScriptMethod(241)  # GetShopList
_get_shop_list.restype = _buffer


def GetShopList():
    result = []
    data = _get_shop_list()
    count = _uint.from_buffer(data)
    offset = count.size
    while 42:
        if offset >= len(data) - 1:
            break
        string = _str.from_buffer(data, offset)
        offset += string.size
        result.append(string.value)
    return result


_clear_shop_list = _ScriptMethod(242)  # ClearShopList


def ClearShopList():
    _clear_shop_list()


_auto_buy_extended = _ScriptMethod(243)  # AutoBuyEx
_auto_buy_extended.argtypes = [_ushort,  # ItemType
                               _ushort,  # ItemColor
                               _ushort,  # Quantity
                               _uint,  # Price
                               _str]  # ItemName


def AutoBuyEx(ItemType, ItemColor, Quantity, Price, ItemName):
    _auto_buy_extended(ItemType, ItemColor, Quantity, Price, ItemName)


_get_auto_buy_delay = _ScriptMethod(244)  # GetAutoBuyDelay
_get_auto_buy_delay.restype = _ushort


def GetAutoBuyDelay():
    return _get_auto_buy_delay()


_set_auto_buy_delay = _ScriptMethod(245)  # SetAutoBuyDelay
_set_auto_buy_delay.argtypes = [_ushort]  # Value


def SetAutoBuyDelay(Value):
    _set_auto_buy_delay(Value)


_get_auto_sell_delay = _ScriptMethod(246)  # GetAutoSellDelay
_get_auto_sell_delay.restype = _ushort


def GetAutoSellDelay():
    return _get_auto_sell_delay()


_set_auto_sell_delay = _ScriptMethod(247)  # SetAutoSellDelay
_set_auto_sell_delay.argtypes = [_ushort]  # Value


def SetAutoSellDelay(Value):
    _set_auto_sell_delay(Value)


_auto_sell = _ScriptMethod(248)  # AutoSell
_auto_sell.argtypes = [_ushort,  # ItemType
                       _ushort,  # ItemColor
                       _ushort]  # Quantity


def AutoSell(ItemType, ItemColor, Quantity):
    _auto_sell(ItemType, ItemColor, Quantity)


_request_stats = _ScriptMethod(249)  # RequestStats
_request_stats.argtypes = [_uint]  # ObjID


def RequestStats(ObjID):
    _request_stats(ObjID)


_help_request = _ScriptMethod(250)  # HelpRequest


def HelpRequest():
    _help_request()


_quest_request = _ScriptMethod(251)  # QuestRequest


def QuestRequest():
    _quest_request()


_rename_mobile = _ScriptMethod(252)  # RenameMobile
_rename_mobile.argtypes = [_uint,  # Mob_ID
                           _str]  # NewName


def RenameMobile(Mob_ID, NewName):
    _rename_mobile(Mob_ID, NewName)


_mobile_can_be_renamed = _ScriptMethod(253)  # MobileCanBeRenamed
_mobile_can_be_renamed.restype = _bool
_mobile_can_be_renamed.argtypes = [_uint]  # Mob_ID


def MobileCanBeRenamed(Mob_ID):
    return _mobile_can_be_renamed(Mob_ID)


_lock_stat = _ScriptMethod(254)  # ChangeStatLockState
_lock_stat.argtypes = [_ubyte,  # statNum
                       _ubyte]  # statState


def SetStatState(statNum, statState):
    _lock_stat(statNum, statState)


_get_static_art_bitmap = _ScriptMethod(255)  # GetStaticArtBitmap
_get_static_art_bitmap.restype = _buffer  # Bitmap file in bytes
_get_static_art_bitmap.argtypes = [_uint,  # Id
                                   _ushort]  # Hue


def GetStaticArtBitmap(Id, Hue):
    return _get_static_art_bitmap(Id, Hue)


_print_script_methods = _ScriptMethod(256)  # PrintScriptMethodsList
_print_script_methods.argtypes = [_str,  # FileName
                                  _bool]  # SortedList


def PrintScriptMethodsList(FileName, SortedList):
    _print_script_methods(FileName, SortedList)


_alarm = _ScriptMethod(257)  # SetAlarm


def Alarm():
    _alarm()


_uo_say = _ScriptMethod(308)  # SendTextToUO
_uo_say.argtypes = [_str]  # Text


def UOSay(Text):
    _uo_say(Text)


_uo_say_color = _ScriptMethod(309)  # SendTextToUOColor
_uo_say_color.argtypes = [_str,  # Text
                          _ushort]  # Color


def UOSayColor(Text, Color):
    _uo_say_color(Text, Color)


_reg_stealth = 0, '0', 'reg_stealth', 'stealth'
_reg_char = 1, '1', 'reg_char', 'char'

_set_global = _ScriptMethod(310)  # SetGlobal
_set_global.argtypes = [_ubyte,  # GlobalRegion
                        _str,  # VarName
                        _str]  # VarValue


def SetGlobal(GlobalRegion, VarName, VarValue):
    if isinstance(GlobalRegion, str):
        GlobalRegion = GlobalRegion.lower()
    for region in _reg_stealth, _reg_char:
        if GlobalRegion in region:
            _set_global(region[0], VarName, VarValue)
            break
    else:
        raise ValueError('GlobalRegion must be "stealth" or "char".')


_get_global = _ScriptMethod(311)
_get_global.restype = _str
_get_global.argtypes = [_ubyte,  # GlobalRegion
                        _str]  # VarName


def GetGlobal(GlobalRegion, VarName):
    if isinstance(GlobalRegion, str):
        GlobalRegion = GlobalRegion.lower()
    for region in _reg_stealth, _reg_char:
        if GlobalRegion in region:
            return _get_global(region[0], VarName)
    else:
        raise ValueError('GlobalRegion must be "stealth" or "char".')


_console_entry_reply = _ScriptMethod(312)
_console_entry_reply.argtypes = [_str]  # Text


def ConsoleEntryReply(Text):
    _console_entry_reply(Text)


_console_entry_unicode_reply = _ScriptMethod(313)  # ConsoleEntryUnicodeReply
_console_entry_unicode_reply.argtypes = [_str]  # Text


def ConsoleEntryUnicodeReply(Text):
    _console_entry_unicode_reply(Text)


_game_server_ip_string = _ScriptMethod(341)  # GameServerIPString
_game_server_ip_string.restype = _str


def GameServerIPString():
    return _game_server_ip_string()


_easyuo_sub_key = 'Software\\EasyUO'


def SetEasyUO(num, Regvalue):
    if b'' == '':  # py2
        import _winreg as winreg
    else:
        import winreg
    key = winreg.HKEY_CURRENT_USER
    access = winreg.KEY_WRITE
    with winreg.OpenKey(key, _easyuo_sub_key, 0, access) as easyuo_key:
        winreg.SetValueEx(easyuo_key, '*' + str(num), 0, winreg.REG_SZ,
                          Regvalue)


def GetEasyUO(num):
    if b'' == '':  # py2
        import _winreg as winreg
    else:
        import winreg
    key = winreg.HKEY_CURRENT_USER
    access = winreg.KEY_READ
    with winreg.OpenKey(key, _easyuo_sub_key, 0, access) as easyuo_key:
        type_, data = winreg.QueryValueEx(easyuo_key, '*' + str(num))
    return data


def EUO2StealthType(EUO):
    # TODO: 2 and 3 compatible code: int(codecs.encode(b'A', 'hex'), 16)
    res = 0
    multi = 1
    for char in EUO:
        if b'' == '':  # py2
            tmp = int(char.encode('hex'), 16)
        else:
            tmp = int.from_bytes(char.encode(), 'little')
        res += multi * (tmp - 65)
        multi *= 26
    res = (res - 7) ^ 0x0045
    return 0 if res > 0xFFFF else res


def EUO2StealthID(EUO):
    # TODO: 2 and 3 compatible code: int(codecs.encode(b'A', 'hex'), 16)
    res = 0
    multi = 1
    for char in EUO:
        if b'' == '':  # py2
            tmp = int(char.encode('hex'), 16)
        else:
            tmp = int.from_bytes(char.encode(), 'little')
        res += multi * (tmp - 65)
        multi *= 26
    return (res - 7) ^ 0x0045


_http_get = _ScriptMethod(258)  # HTTP_Get
_http_get.argtypes = [_str]  # URL


def HTTP_Get(URL):
    _http_get(URL)


_http_post = _ScriptMethod(259)  # HTTP_Post
_http_post.restype = _str
_http_post.argtypes = [_str,  # URL
                       _str]  # PostData


def HTTP_Post(URL, PostData):
    return _http_post(URL, PostData)


_http_body = _ScriptMethod(260)  # HTTP_Body
_http_body.restype = _str


def HTTP_Body():
    return _http_body()


_http_header = _ScriptMethod(261)  # HTTP_Header
_http_header.restype = _str


def HTTP_Header():
    return _http_header()


_party_invite = _ScriptMethod(262)  # InviteToParty
_party_invite.argtypes = [_uint]  # ID


def InviteToParty(ID):
    _party_invite(ID)


_party_kick = _ScriptMethod(263)  # RemoveFromParty
_party_kick.argtypes = [_uint]  # ID


def RemoveFromParty(ID):
    _party_kick(ID)


_party_msg_to = _ScriptMethod(264)  # PartyMessageTo
_party_msg_to.argtypes = [_uint,  # ID
                          _str]  # Msg


def PartyMessageTo(ID, Msg):
    _party_msg_to(ID, Msg)


_party_msg = _ScriptMethod(265)  # PartySay
_party_msg.argtypes = [_str]  # Msg


def PartySay(Msg):
    _party_msg(Msg)


_party_can_loot = _ScriptMethod(266)  # PartyCanLootMe
_party_can_loot.argtypes = [_bool]  # Value


def PartyCanLootMe(Value):
    _party_can_loot(Value)


_party_accept = _ScriptMethod(267)  # PartyAcceptInvite


def PartyAcceptInvite():
    _party_accept()


_party_reject = _ScriptMethod(268)  # PartyDeclineInvite


def PartyDeclineInvite():
    _party_reject()


_party_leave = _ScriptMethod(269)  # PartyLeave


def PartyLeave():
    _party_leave()


_is_in_party = _ScriptMethod(271)  # InParty
_is_in_party.restype = _bool


def InParty():
    return _is_in_party()


_get_party_members = _ScriptMethod(270)  # PartyMembersList
_get_party_members.restype = _buffer  # Array of Cardinal


def PartyMembersList():
    result = []
    data = _get_party_members()
    count = _uint.from_buffer(data)
    if count:
        fmt = '<' + count * 'I'
        result.extend(_struct.unpack(fmt, data))
    return result


_get_icq_connection_state = _ScriptMethod(272)  # GetConnectedStatus
_get_icq_connection_state.restype = _bool


def ICQConnected():
    return _get_icq_connection_state()


_icq_connect = _ScriptMethod(273)  # ICQ_Connect
_icq_connect.argtypes = [_uint,  # UIN
                         _str]  # Password


def ICQConnect(UIN, Password):
    _icq_connect(UIN, Password)


_icq_disconnect = _ScriptMethod(274)  # ICQ_Disconnect


def ICQDisconnect():
    _icq_disconnect()


_icq_set_status = _ScriptMethod(275)  # ICQ_SetStatus
_icq_set_status.argtypes = [_ubyte]  # Num


def ICQSetStatus(Num):
    _icq_set_status(Num)


_icq_set_x_status = _ScriptMethod(276)  # ICQ_SetXStatus
_icq_set_x_status.argtypes = [_ubyte]  # Num


def ICQSetXStatus(Num):
    _icq_set_x_status(Num)


_icq_send_message = _ScriptMethod(277)  # ICQ_SendText
_icq_send_message.argtypes = [_uint,  # DestinationUIN
                              _str]  # Text


def ICQSendText(DestinationUIN, Text):
    _icq_send_message(DestinationUIN, Text)


_messengers = {0: 1,  # default - telegram
               1: 1, 'Telegram': 1, 'telegram': 1,
               2: 2, 'Viber': 2, 'viber': 2,
               3: 3, 'Discord': 3, 'discord': 3}

_messenger_get_connected = _ScriptMethod(501)  # Messenger_GetConnected
_messenger_get_connected.restype = _bool
_messenger_get_connected.argtypes = [_ubyte]  # MesID


def MessengerGetConnected(MesID):
    if MesID not in _messengers.keys():
        error = 'MessengerGetConnected: MesID must be "Telegram", "Viber" or "Discord"'
        raise ValueError(error)
    return _messenger_get_connected(_messengers[MesID])


_messenger_set_connected = _ScriptMethod(502)  # Messenger_SetConnected
_messenger_set_connected.argtypes = [_ubyte,  # MesID
                                     _bool]  # Value


def MessengerSetConnected(MesID, Value):
    if MesID not in _messengers.keys():
        error = 'MessengerGetConnected: MesID must be "Telegram", "Viber" or "Discord"'
        raise ValueError(error)
    _messenger_set_connected(_messengers[MesID], Value)


_messenger_get_token = _ScriptMethod(503)  # Messenger_GetToken
_messenger_get_token.restype = _str
_messenger_get_token.argtypes = [_ubyte]  # MesID


def MessengerGetToken(MesID):
    if MesID not in _messengers.keys():
        error = 'MessengerGetConnected: MesID must be "Telegram", "Viber" or "Discord"'
        raise ValueError(error)
    return _messenger_get_token(_messengers[MesID])


_messenger_set_token = _ScriptMethod(504)  # Messenger_SetToken
_messenger_set_token.argtypes = [_ubyte,  # MesID
                                 _str]  # Value


def MessengerSetToken(MesID, Value):
    if MesID not in _messengers.keys():
        error = 'MessengerGetConnected: MesID must be "Telegram", "Viber" or "Discord"'
        raise ValueError(error)
    _messenger_set_token(_messengers[MesID], Value)


_messenger_get_name = _ScriptMethod(505)  # Messenger_GetName
_messenger_get_name.restype = _str
_messenger_get_name.argtypes = [_ubyte]  # MesID


def MessengerGetName(MesID):
    if MesID not in _messengers.keys():
        error = 'MessengerGetConnected: MesID must be "Telegram", "Viber" or "Discord"'
        raise ValueError(error)
    return _messenger_get_name(_messengers[MesID])


_messenger_send_message = _ScriptMethod(506)  # Messenger_SendMessage
_messenger_send_message.argtypes = [_ubyte,  # MesID
                                    _str,  # Msg
                                    _str]  # UserID


def MessengerSendMessage(MesID, Msg, UserID):
    if MesID not in _messengers.keys():
        error = 'MessengerGetConnected: MesID must be "Telegram", "Viber" or "Discord"'
        raise ValueError(error)
    _messenger_send_message(_messengers[MesID], Msg, UserID)


_tile_groups = {0: 0, 'tfLand': 0, 'tfland': 0, 'Land': 0, 'land': 0,
                1: 1, 'tfStatic': 1, 'tfstatic': 1, 'Static': 1, 'static': 1}

_get_tile_flags = _ScriptMethod(278)  # GetTileFlags
_get_tile_flags.restype = _uint
_get_tile_flags.argtypes = [_ubyte,  # TileGroup
                            _ushort]  # Tile


def GetTileFlags(TileGroup, Tile):
    if TileGroup not in _tile_groups.keys():
        raise ValueError('GetTileFlags: TileGroup must be "Land" or "Static"')
    group = _tile_groups[TileGroup]
    return _get_tile_flags(group, Tile)


_uint_to_flags = _ScriptMethod(350)  # ConvertIntegerToFlags
_uint_to_flags.restype = _buffer
_uint_to_flags.argtypes = [_ubyte,  # Group
                           _uint]  # Flags


def ConvertIntegerToFlags(Group, Flags):
    if Group not in _tile_groups.keys():
        raise ValueError('GetTileFlags: Group must be "Land" or "Static"')
    result = []
    data = _uint_to_flags(_tile_groups[Group], Flags)
    count = _uint.from_buffer(data)
    offset = count.size
    while 42:
        if offset >= len(data) - 1:
            break
        string = _str.from_buffer(data, offset)
        offset += string.size
        result.append(string.value)
    return result


_get_land_tile_data = _ScriptMethod(280)  # GetLandTileData
_get_land_tile_data.restype = _buffer  # TLandTileData
_get_land_tile_data.argtypes = [_ushort]  # Tile


def GetLandTileData(Tile):
    result = {}
    data = _get_land_tile_data(Tile)
    if data:
        result['Flags'] = ConvertIntegerToFlags(0, _uint.from_buffer(data))
        result['Flags2'] = ConvertIntegerToFlags(0, _uint.from_buffer(data[4:]))
        result['TextureID'] = _ushort.from_buffer(data[8:])
        length = _uint.from_buffer(data[10:])
        result['Name'] = data[14:14 + length].rstrip(b'\x00')
        if b'' != '':  # py3
            result['Name'] = result['Name'].decode()
    return result


_get_static_tile_data = _ScriptMethod(281)  # GetStaticTileData
_get_static_tile_data.restype = _buffer  # TStaticTileDataNew
_get_static_tile_data.argtypes = [_ushort]  # Tile


def GetStaticTileData(Tile):
    result = {}
    data = _get_static_tile_data(Tile)
    if data:
        result['Flags'] = ConvertIntegerToFlags(1, _ulong.from_buffer(data))
        result['Weight'] = _int.from_buffer(data, 4)
        result['Height'] = _int.from_buffer(data, 8)
        result['RadarColorRGBA'] = _struct.unpack_from('<4B', data, 12)
        length = _uint.from_buffer(data, 16)
        result['Name'] = data[20: 20 + length].rstrip(b'\x00')
        if b'' != '':  # py3
            result['Name'] = result['Name'].decode()
    return result


_get_cell = _ScriptMethod(13)  # GetCell
_get_cell.restype = _buffer  # TMapCell
_get_cell.argtypes = [_ushort,  # X
                      _ushort,  # Y
                      _ubyte]  # WorldNum


def GetCell(X, Y, WorldNum):
    result = {}
    data = _get_cell(X, Y, WorldNum)
    if data:
        fmt = '<Hb'
        keys = 'Tile', 'Z'
        values = _struct.unpack(fmt, data)
        result.update(zip(keys, values))
    return result


_get_layer_count = _ScriptMethod(282)  # GetLayerCount
_get_layer_count.restype = _ubyte
_get_layer_count.argtypes = [_ushort,  # X
                             _ushort,  # Y
                             _ubyte]  # WorldNum


def GetLayerCount(X, Y, WorldNum):
    return _get_layer_count(X, Y, WorldNum)


_read_static_xy = _ScriptMethod(283)  # ReadStaticsXY
_read_static_xy.restype = _buffer  # Array of TStaticItemRealXY
_read_static_xy.argtypes = [_ushort,  # X
                            _ushort,  # Y
                            _ubyte]  # WorldNum


def ReadStaticsXY(X, Y, WorldNum):
    result = []
    data = _read_static_xy(X, Y, WorldNum)
    count = _uint.from_buffer(data)
    fmt = '<3HbH'
    size = _struct.calcsize(fmt)
    keys = 'Tile', 'X', 'Y', 'Z', 'Color'
    for i in range(count):
        values = _struct.unpack_from(fmt, data, 4 + i * size)
        item = dict(zip(keys, values))
        result.append(item)

    # if count:
    #     keys = 'Tile', 'X', 'Y', 'Z', 'Color'
    #     for pos in range(0, len(data), _struct.calcsize(fmt)):
    #         values = _struct.unpack_from(fmt, data, pos)
    #         item = dict(zip(keys, values))
    #         result.append(item)
    return result


_get_surface_z = _ScriptMethod(284)  # GetSurfaceZ
_get_surface_z.restype = _byte
_get_surface_z.argtypes = [_ushort,  # X
                           _ushort,  # Y
                           _ubyte]  # WorldNum


def GetSurfaceZ(X, Y, WorldNum):
    return _get_surface_z(X, Y, WorldNum())


_is_cell_passable = _ScriptMethod(285)  # IsWorldCellPassable
_is_cell_passable.restype = _buffer  # Boolean, ShortInt  4 bytes
_is_cell_passable.argtypes = [_ushort,  # CurrX
                              _ushort,  # CurrY
                              _byte,  # CurrZ
                              _ushort,  # DestX
                              _ushort,  # DestY
                              _ubyte]  # WorldNum


def IsWorldCellPassable(CurrX, CurrY, CurrZ, DestX, DestY, WorldNum):
    data = _is_cell_passable(CurrX, CurrY, CurrZ, DestX, DestY, WorldNum)
    return _struct.unpack('<?b', data)


_get_statics_array = _ScriptMethod(286)  # GetStaticTilesArray
_get_statics_array.restype = _buffer  # Array of TFoundTile
_get_statics_array.argtypes = [_ushort,  # Xmin
                               _ushort,  # Ymin
                               _ushort,  # Xmax
                               _ushort,  # Ymax
                               _ubyte,  # WorldNum
                               _uint,  # Len
                               _buffer]  # TileTypes: Array of Word


def GetStaticTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, TileTypes):
    if not _iterable(TileTypes):
        TileTypes = [TileTypes]
    result = []
    data = _get_statics_array(
        Xmin, Ymin, Xmax, Ymax, WorldNum, len(TileTypes),
        _struct.pack('<' + 'H' * len(TileTypes), *TileTypes)
    )
    count = _uint.from_buffer(data)
    fmt = '<3Hb'
    size = _struct.calcsize(fmt)
    for i in range(count):
        result.append(_struct.unpack_from(fmt, data, count.size + i * size))
    return result


_get_lands_array = _ScriptMethod(287)  # GetLandTilesArray
_get_lands_array.restype = _buffer  # Array of TFoundTile
_get_lands_array.argtypes = [_ushort,  # Xmin
                             _ushort,  # Ymin
                             _ushort,  # Xmax
                             _ushort,  # Ymax
                             _ubyte,  # WorldNum
                             _uint,  # Len
                             _buffer]  # TileTypes: Array of Word


def GetLandTilesArray(Xmin, Ymin, Xmax, Ymax, WorldNum, TileTypes):
    if not _iterable(TileTypes):
        TileTypes = [TileTypes]
    result = []
    data = _get_lands_array(
        Xmin, Ymin, Xmax, Ymax, WorldNum, len(TileTypes),
        _struct.pack('<' + 'H' * len(TileTypes), *TileTypes)
    )
    count = _uint.from_buffer(data)
    fmt = '<3Hb'
    size = _struct.calcsize(fmt)
    for i in range(count):
        result.append(_struct.unpack_from(fmt, data, count.size + i * size))
    return result


_client_print = _ScriptMethod(289)  # ClientPrint
_client_print.argtypes = [_str]  # Text


def ClientPrint(Text):
    _client_print(Text)


_client_print_ex = _ScriptMethod(290)  # ClientPrintEx
_client_print_ex.argtypes = [_uint,  # SenderID
                             _ushort,  # Color
                             _ushort,  # Font
                             _str]  # Text


def ClientPrintEx(SenderID, Color, Font, Text):
    _client_print_ex(SenderID, Color, Font, Text)


_wnd = {0: 0, '0': 0, 'wtpaperdoll': 0, 'paperdoll': 0,
        1: 1, '1': 1, 'wtstatus': 1, 'status': 1,
        2: 2, '2': 2, 'wtcharprofile': 2, 'charprofile': 2, 'profile': 2,
        3: 3, '3': 3, 'wtcontainer': 3, 'container': 3}

_close_client_ui_window = _ScriptMethod(291)  # CloseClientUIWindow
_close_client_ui_window.argtypes = [_ubyte,  # UIWindowType
                                    _uint]  # ID


def CloseClientUIWindow(UIWindowType, ID):
    if isinstance(UIWindowType, str):
        UIWindowType = UIWindowType.lower()
    if UIWindowType not in _wnd.keys():
        raise ValueError('CloseClientUIWindow: UIWindowType must be '
                         '"Paperdoll", "Status", "CharProfile" or "Container"')
    _close_client_ui_window(_wnd[UIWindowType], ID)


_client_target_object_request = _ScriptMethod(292)  # ClientRequestObjectTarget


def ClientRequestObjectTarget():
    _client_target_object_request()


_client_target_tile_request = _ScriptMethod(293)  # ClientRequestTileTarget


def ClientRequestTileTarget():
    _client_target_tile_request()


_client_is_target_response = _ScriptMethod(294)  # ClientTargetResponsePresent
_client_is_target_response.restype = _bool


def ClientTargetResponsePresent():
    return _client_is_target_response()


_client_target_response = _ScriptMethod(295)  # ClientTargetResponse
_client_target_response.restype = _buffer  # TTargetInfo


def ClientTargetResponse():
    result = {}
    data = _client_target_response()
    if data:
        fmt = '<I3Hb'
        keys = 'ID', 'Tile', 'X', 'Y', 'Z'
        values = _struct.unpack(fmt, data)
        result.update(zip(keys, values))
    return result


def WaitForClientTargetResponse(MaxWaitTimeMS):
    end = _time.time() + MaxWaitTimeMS / 1000
    while _time.time() < end:
        if ClientTargetResponsePresent():
            return True
        Wait(10)
    return False


_check_lag_begin = _ScriptMethod(297)  # CheckLagBegin
_check_lag_end = _ScriptMethod(298)  # CheckLagEnd
_is_check_lag_ended = _ScriptMethod(299)  # IsCheckLagEnd
_is_check_lag_ended.restype = _bool


def CheckLag(timeoutMS=10000):
    end = _time.time() + timeoutMS / 1000
    result = False
    _check_lag_begin()
    while _time.time() < end:
        if _is_check_lag_ended():
            return True
    _check_lag_end()
    return result


_get_quest_arrow = _ScriptMethod(300)  # GetQuestArrow
_get_quest_arrow.restype = _buffer  # TPoint


def GetQuestArrow():
    data = _get_quest_arrow()
    if data:
        return _struct.unpack('<ii', data)
    return ()


_get_silent_mode = _ScriptMethod(302)  # GetSilentMode
_get_silent_mode.restype = _bool


def GetSilentMode():
    return _get_silent_mode()


_clear_info_window = _ScriptMethod(348)  # ClearInfoWindow


def ClearInfoWindow():
    _clear_info_window()


_set_silent_mode = _ScriptMethod(301)  # SetSilentMode
_set_silent_mode.argtypes = [_bool]  # Value


def SetSilentMode(Value):
    _set_silent_mode(Value)


_fill_info_window = _ScriptMethod(303)  # FillInfoWindow
_fill_info_window.argtypes = [_str]  # s


def FillNewWindow(s):
    _fill_info_window(s)


_get_stealth_path = _ScriptMethod(305)  # GetStealthPath
_get_stealth_path.restype = _str


def StealthPath():
    return _get_stealth_path()


def CurrentScriptPath():
    return __file__


_get_stealth_profile_path = _ScriptMethod(306)  # GetStealthProfilePath
_get_stealth_profile_path.restype = _str


def GetStealthProfilePath():
    return _get_stealth_profile_path()


_get_shard_path = _ScriptMethod(307)  # GetShardPath
_get_shard_path.restype = _str


def GetShardPath():
    return _get_shard_path()


_step = _ScriptMethod(324)  # Step
_step.restype = _ubyte
_step.argtypes = [_ubyte,  # Direction
                  _bool]  # Running


def Step(Direction, Running=False):
    return _step(Direction, Running)


_step_q = _ScriptMethod(325)  # StepQ
_step_q.restype = _int
_step_q.argtypes = [_ubyte,  # Direction
                    _bool]  # Running


def StepQ(Direction, Running):
    return _step_q(Direction, Running)


_move_xyz = _ScriptMethod(326)  # MoveXYZ
_move_xyz.restype = _bool
_move_xyz.argtypes = [_ushort,  # Xdst
                      _ushort,  # Ydst
                      _byte,  # Zdst
                      _int,  # AccuracyXY
                      _int,  # AccuracyZ
                      _bool]  # Running


def MoveXYZ(Xdst, Ydst, Zdst, AccuracyXY, AccuracyZ, Running):
    return _move_xyz(Xdst, Ydst, Zdst, AccuracyXY, AccuracyZ, Running)


def newMoveXYZ(Xdst, Ydst, Zdst, AccuracyXY, AccuracyZ, Running, Callback=None):
    def debug(msg):
        if MoveXYZ.debug:
            AddToSystemJournal('MoveXYZ: ' + msg)

    def step(dir, run):
        while 42:  # while True
            step = StepQ(dir, run)
            if step == -2 or step >= 0:
                return step >= 0
            Wait(10)

    if not hasattr(MoveXYZ, 'debug'):
        MoveXYZ.debug = False

    find_path = True
    while 42:  # while True
        # pause while not connected
        while not Connected():
            Wait(100)
        # try to find a path if required
        if find_path:
            find_path = False
            path = GetPathArray3D(PredictedX(), PredictedY(), PredictedZ(),
                                  Xdst, Ydst, Zdst,
                                  WorldNum(), AccuracyXY, AccuracyZ, Running)
            # there is no path to a target location
            if len(path) <= 0:
                debug('There is no path to a target location.')
                return False
            debug('Path found. Length = ' + str(len(path)))
        # check path passability for a few steps
        cx, cy, cz = PredictedX(), PredictedY(), PredictedZ()
        for i in range(4):
            try:
                x, y, z = path[i]
                if IsWorldCellPassable(cx, cy, cz, x, y, WorldNum()):
                    cx, cy, cz = x, y, z
                else:
                    debug('Point ({0}, {1}, {2}) is not passable.'.format(x, y,
                                                                          z))
                    find_path = True
                    break
            except IndexError:
                break
        if find_path:
            continue
        # stamina check
        if not Dead() and Stam() < GetMoveCheckStamina():
            Wait(100)
        # lets walk :)
        mx, my = PredictedX(), PredictedY()
        x, y, z = path.pop(0)
        dx = mx - x
        dy = my - y
        dir = CalcDir(mx, my, x, y)
        # if something wrong
        if (dx == 0 and dy == 0) or (abs(dx) > 1 or abs(dy) > 1) or dir == 100:
            debug('dx = {0}, dy = {1}, dir = {2}'.format(dx, dy, dir))
            find_path = True
            continue
        # try to turn if required
        if PredictedDirection() != dir:
            if not step(dir, Running):
                find_path = True
                continue
        # try to do a step
        if not step(dir, Running):
            find_path = True
            continue
        # call a callback object if it is not None
        # if callback will returns False - return
        if Callback is not None:
            if not Callback(x, y, z):
                return False
        # looks like it is done
        if not path:
            mx, my = PredictedX(), PredictedY()
            # ensure this
            if abs(mx - Xdst) <= AccuracyXY and abs(my - Ydst) <= AccuracyXY:
                debug('Location reached!')
                return True
            # nope (
            debug('Wtf? Recompute path.')
            find_path = True


def newMoveXY(Xdst, Ydst, Optimized, Accuracy, Running):
    return MoveXYZ(Xdst, Ydst, 0, Accuracy, 255, Running)


def NewMoveXY(Xdst, Ydst, Optimized, Accuracy, Running):
    return newMoveXY(Xdst, Ydst, Optimized, Accuracy, Running)


_move_xy = _ScriptMethod(327)  # MoveXY
_move_xy.restype = _bool
_move_xy.argtypes = [_ushort,  # Xdst
                     _ushort,  # Ydst
                     _bool,  # Optimized
                     _int,  # AccuracyXY
                     _bool]  # Running


def MoveXY(Xdst, Ydst, Optimized, Accuracy, Running):
    return _move_xy(Xdst, Ydst, Optimized, Accuracy, Running)


_set_impassable_location = _ScriptMethod(328)  # SetBadLocation
_set_impassable_location.argtypes = [_ushort,  # X
                                     _ushort]  # Y


def SetBadLocation(X, Y):
    _set_impassable_location(X, Y)


_set_passable_location = _ScriptMethod(329)  # SetGoodLocation
_set_passable_location.argtypes = [_ushort,  # X
                                   _ushort]  # Y


def SetGoodLocation(X, Y):
    _set_passable_location(X, Y)


_clear_impassable_locations = _ScriptMethod(330)  # ClearBadLocationList


def ClearBadLocationList():
    _clear_impassable_locations()


_set_impassable_object = _ScriptMethod(331)  # SetBadObject
_set_impassable_object.argtypes = [_ushort,  # Type
                                   _ushort,  # Color
                                   _ubyte]  # Radius


def SetBadObject(Type, Color, Radius):
    _set_impassable_object(Type, Color, Radius)


_clear_impassable_objects = _ScriptMethod(332)  # ClearBadObjectList


def ClearBadObjectList():
    _clear_impassable_objects()


_los_check_type = {1: 1, '1': 1, 'lossphere': 1, 'sphere': 1,
                   2: 2, '2': 2, 'lossphereadv': 2, 'sphereadv': 2,
                   3: 3, '3': 3, 'lospol': 3, 'pol': 3,
                   4: 4, '4': 4, 'losrunuo': 4, 'runuo': 4, 'servuo': 4}

_los_check_options = {0: 0, '0': 0, None: 0,
                      0x100: 0x100,
                      'losspherecheckcorners': 0x100,
                      'spherecheckcorners': 0x100,
                      0x200: 0x200,
                      'lospolusenoshoot': 0x200,
                      'polusenoshoot': 0x200,
                      0x400: 0x400,
                      'lospollosthroughwindow': 0x400,
                      'pollosthroughwindow': 0x400}

_check_los = _ScriptMethod(333)  # CheckLOS
_check_los.restype = _bool
_check_los.argtypes = [_ushort,  # xf
                       _ushort,  # yf
                       _byte,  # zf
                       _ushort,  # xt
                       _ushort,  # yt
                       _byte,  # zt
                       _ubyte,  # WorldNum
                       _ubyte,  # LOSCheckType
                       _uint]  # LOSOptions


def CheckLOS(xf, yf, zf, xt, yt, zt, WorldNum, LOSCheckType, LOSOptions=None):
    if not _iterable(LOSOptions) or isinstance(LOSOptions, str):
        LOSOptions = [LOSOptions]
    if isinstance(LOSCheckType, str):
        LOSCheckType = LOSCheckType.lower()
    if LOSCheckType not in _los_check_type.keys():
        raise ValueError('CheckLOS: LOSCheckType must be "Sphere", "SphereAdv"'
                         ', "Pol" or "RunUO".')
    options = 0
    for option in LOSOptions:
        if isinstance(option, str):
            option = option.lower()
        if option not in _los_check_options.keys():
            raise ValueError('CheckLOS: LOSOptions must be set of '
                             '"SphereCheckCorners", "PolUseNoShoot", '
                             '"PolLosThroughWindow" or None.')
        options |= _los_check_options[option]
    return _check_los(xf, yf, zf, xt, yt, zt, WorldNum, LOSCheckType, options)


_get_path_array = _ScriptMethod(334)  # GetPathArray
_get_path_array.restype = _buffer  # Array of TMyPoint
_get_path_array.argtypes = [_ushort,  # DestX
                            _ushort,  # DestY
                            _bool,  # Optimized
                            _int]  # Accuracy


def GetPathArray(DestX, DestY, Optimized, Accuracy):
    result = []
    data = _get_path_array(DestX, DestY, Optimized, Accuracy)
    count = _uint.from_buffer(data)
    fmt = '<2Hb'
    size = _struct.calcsize(fmt)
    for i in range(count):
        result.append(_struct.unpack_from(fmt, data, count.size + i * size))
    return result


_get_path_array_3d = _ScriptMethod(335)  # GetPathArray3D
_get_path_array_3d.restype = _buffer  # Array of TMyPoint
_get_path_array_3d.argtypes = [_ushort,  # StartX
                               _ushort,  # StartY
                               _byte,  # StartZ
                               _ushort,  # FinishX
                               _ushort,  # FinishY
                               _byte,  # FinishZ
                               _ubyte,  # WorldNum
                               _int,  # AccuracyXY
                               _int,  # AccuracyZ
                               _bool]  # Run


def GetPathArray3D(StartX, StartY, StartZ, FinishX, FinishY, FinishZ, WorldNum,
                   AccuracyXY, AccuracyZ, Run):
    result = []
    data = _get_path_array_3d(StartX, StartY, StartZ, FinishX, FinishY,
                              FinishZ, WorldNum, AccuracyXY, AccuracyZ, Run)
    count = _uint.from_buffer(data)
    fmt = '<2Hb'
    size = _struct.calcsize(fmt)
    for i in range(count):
        result.append(_struct.unpack_from(fmt, data, count.size + i * size))
    return result


def Dist(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    return dx if dx > dy else dy


def CalcCoord(x, y, Dir):
    if Dir > 7:
        return x, y
    dirs = {0: (0, -1),
            1: (1, -1),
            2: (1, 0),
            3: (1, 1),
            4: (0, 1),
            5: (-1, 1),
            6: (-1, 0),
            7: (-1, -1)}
    dx, dy = dirs[Dir]
    return x + dx, y + dy


def CalcDir(Xfrom, Yfrom, Xto, Yto):
    dx = abs(Xto - Xfrom)
    dy = abs(Yto - Yfrom)
    if dx == dy == 0:
        return 100
    elif (dx / (dy + 0.1)) >= 2:
        return 6 if Xfrom > Xto else 2
    elif (dy / (dx + 0.1)) >= 2:
        return 0 if Yfrom > Yto else 4
    elif Xfrom > Xto:
        return 7 if Yfrom > Yto else 5
    elif Xfrom < Xto:
        return 1 if Yfrom > Yto else 3


_set_run_unmount_timer = _ScriptMethod(316)  # SetRunUnmountTimer
_set_run_unmount_timer.argtypes = [_ushort]  # Value


def SetRunUnmountTimer(Value):
    _set_run_unmount_timer(Value)


_set_walk_mount_timer = _ScriptMethod(317)  # SetWalkMountTimer
_set_walk_mount_timer.argtypes = [_ushort]  # Value


def SetWalkMountTimer(Value):
    _set_walk_mount_timer(Value)


_set_run_mount_timer = _ScriptMethod(318)  # SetRunMountTimer
_set_run_mount_timer.argtypes = [_ushort]  # Value


def SetRunMountTimer(Value):
    _set_run_mount_timer(Value)


_set_walk_unmount_timer = _ScriptMethod(319)  # SetWalkUnmountTimer
_set_walk_unmount_timer.argtypes = [_ushort]  # Value


def SetWalkUnmountTimer(Value):
    _set_walk_unmount_timer(Value)


_get_run_mount_timer = _ScriptMethod(320)  # GetRunMountTimer
_get_run_mount_timer.restype = _ushort


def GetRunMountTimer():
    return _get_run_mount_timer()


_get_walk_mount_timer = _ScriptMethod(321)  # GetWalkMountTimer
_get_walk_mount_timer.restype = _ushort


def GetWalkMountTimer():
    return _get_walk_mount_timer()


_get_run_unmount_timer = _ScriptMethod(322)  # GetRunUnmountTimer
_get_run_unmount_timer.restype = _ushort


def GetRunUnmountTimer():
    return _get_run_unmount_timer()


_get_walk_unmount_timer = _ScriptMethod(323)  # GetWalkUnmountTimer
_get_walk_unmount_timer.restype = _ushort


def GetWalkUnmountTimer():
    return _get_walk_unmount_timer()


_get_last_step_q_used_door = _ScriptMethod(344)  # GetLastStepQUsedDoor
_get_last_step_q_used_door.restype = _uint


def GetLastStepQUsedDoor():
    return _get_last_step_q_used_door()


_stop_mover = _ScriptMethod(353)  # MoverStop


def StopMover():
    _stop_mover()


def MoverStop():
    StopMover()


_set_reconnector_ext = _ScriptMethod(354)  # SetARExtParams
_set_reconnector_ext.argtypes = [_str,  # ShardName
                                 _str,  # CharName
                                 _bool]  # UseAtEveryConnect


def SetARExtParams(ShardName, CharName, UseAtEveryConnect):
    _set_reconnector_ext(ShardName, CharName, UseAtEveryConnect)


_use_item_on_mobile = _ScriptMethod(359)  # SCUseItemOnMobile
_use_item_on_mobile.argtypes = [_uint,  # ItemSerial
                                _uint]  # TargetSerial


def UseItemOnMobile(ItemSerial, TargetSerial):
    _use_item_on_mobile(ItemSerial, TargetSerial)


_bandage_self = _ScriptMethod(360)  # SCBandageSelf


def BandageSelf():
    _bandage_self()


_global_chat_join_channel = _ScriptMethod(361)  # SCGlobalChatJoinChannel
_global_chat_join_channel.argtypes = [_str]  # ChName


def GlobalChatJoinChannel(ChName):
    _global_chat_join_channel(ChName)


global_chat_leave_channel = _ScriptMethod(362)  # SCGlobalChatLeaveChannel


def GlobalChatLeaveChannel():
    global_chat_leave_channel()


_global_chat_send_msg = _ScriptMethod(363)  # SCGlobalChatSendMsg
_global_chat_send_msg.argtypes = [_str]  # MsgText


def GlobalChatSendMsg(MsgText):
    _global_chat_send_msg(MsgText)


global_chat_active_channel = _ScriptMethod(364)  # SCGlobalChatActiveChannel
global_chat_active_channel.restype = _str


def GlobalChatActiveChannel():
    return global_chat_active_channel()


global_chat_channel_list = _ScriptMethod(365)  # SCGlobalChatChannelsList
global_chat_channel_list.restype = _buffer


def GlobalChatChannelsList():
    result = []
    data = global_chat_channel_list()
    count = _uint.from_buffer(data)
    offset = count.size
    for i in range(count):
        string = _str.from_buffer(data, offset)
        offset += string.size
        result.append(string.value)
    return result


_set_open_doors = _ScriptMethod(400)  # SetMoveOpenDoor
_set_open_doors.argtypes = [_bool]  # Value


def SetMoveOpenDoor(Value):
    _set_open_doors(Value)


_get_open_doors = _ScriptMethod(401)  # GetMoveOpenDoor
_get_open_doors.restype = _bool


def GetMoveOpenDoor():
    return _get_open_doors()


_set_move_through_npc = _ScriptMethod(402)  # SetMoveThroughNPC
_set_move_through_npc.argtypes = [_ushort]  # Value


def SetMoveThroughNPC(Value):
    _set_move_through_npc(Value)


_get_move_through_npc = _ScriptMethod(403)  # GetMoveThroughNPC
_get_move_through_npc.restype = _ushort


def GetMoveThroughNPC():
    return _get_move_through_npc()


_set_move_through_corner = _ScriptMethod(404)  # SetMoveThroughCorner
_set_move_through_corner.argtypes = [_bool]  # Value


def SetMoveThroughCorner(Value):
    _set_move_through_corner(Value)


_get_move_through_corner = _ScriptMethod(405)  # GetMoveThroughCorner
_get_move_through_corner.restype = _bool


def GetMoveThroughCorner():
    return _get_move_through_corner()


_set_move_heuristic_mult = _ScriptMethod(406)  # SetMoveHeuristicMult
_set_move_heuristic_mult.argtypes = [_int]  # Value


def SetMoveHeuristicMult(Value):
    _set_move_heuristic_mult(Value)


_get_move_heuristic_mult = _ScriptMethod(407)  # GetMoveHeuristicMult
_get_move_heuristic_mult.restype = _int


def GetMoveHeuristicMult():
    return _get_move_heuristic_mult()


_set_move_check_stamina = _ScriptMethod(408)  # SetMoveCheckStamina
_set_move_check_stamina.argtypes = [_ushort]  # Value


def SetMoveCheckStamina(Value):
    _set_move_check_stamina(Value)


_get_move_check_stamina = _ScriptMethod(409)  # GetMoveCheckStamina
_get_move_check_stamina.restype = _ushort


def GetMoveCheckStamina():
    return _get_move_check_stamina()


_set_move_turn_cost = _ScriptMethod(410)  # SetMoveTurnCost
_set_move_turn_cost.argtypes = [_int]  # Value


def SetMoveTurnCost(Value):
    _set_move_turn_cost(Value)


_get_move_turn_cost = _ScriptMethod(411)  # GetMoveTurnCost
_get_move_turn_cost.restype = _int


def GetMoveTurnCost():
    return _get_move_turn_cost()


_set_move_between_two_corners = _ScriptMethod(412)  # SetMoveBetweenTwoCorners
_set_move_between_two_corners.argtypes = [_bool]  # Value


def SetMoveBetweenTwoCorners(Value):
    _set_move_between_two_corners(Value)


_get_move_between_two_corners = _ScriptMethod(413)  # GetMoveBetweenTwoCorners
_get_move_between_two_corners.restype = _bool


def GetMoveBetweenTwoCorners():
    return _get_move_between_two_corners()


def StartStealthSocketInstance(*args, **kwargs):
    Wait(10)


def CorrectDisconnection():
    _get_connection().close()


def PlayWav(FileName):
    import platform
    if platform.system() == 'Windows':
        import winsound
        winsound.PlaySound(FileName, winsound.SND_FILENAME)
    else:
        error = 'PlayWav supports only windows.'
        AddToSystemJournal(error)


_get_multis = _ScriptMethod(347)  # GetMultis
_get_multis.restype = _buffer


def GetMultis():
    data = _get_multis()
    result = []
    count = _uint.from_buffer(data)
    fmt = '<I2Hb6H'
    size = _struct.calcsize(fmt)
    keys = ("ID", "X", "Y", "Z",
            "XMin", "XMax", "YMin", "YMax",
            "Width", "Height")
    for i in range(count):
        obj = dict(
            zip(keys, _struct.unpack_from(fmt, data, i * size + count.size)))
        result.append(obj)
    return result


_get_menu_items_ex = _ScriptMethod(358)  # GetMenuItemsEx
_get_menu_items_ex.restype = _buffer
_get_menu_items_ex.argtypes = [_str]


def GetMenuItemsEx(MenuCaption):
    """
    GetMenuItemsEx(MenuCaption: str) => Array of MenuItems
    MenuItems:
        model: int (item type i guess)
        color: int
        text: str
    Example:
        menu_items = GetMenuItemsEx('Inscription items')
        print(menu_items[0].text)
        >> 1 Blank scroll
    """

    class MenuItems:
        model = None
        color = None
        text = None

        def __str__(self):
            template = 'Model: {0}, Color: {1}, Text: {2}'
            return '{ ' + template.format(hex(self.model), hex(self.color),
                                          self.text) + ' }'

        def __repr__(self):
            return self.__str__()

    data = _get_menu_items_ex(MenuCaption)
    result = []
    count = _struct.unpack_from('<I', data, 0)
    offset = count.size
    while offset < len(data):
        model, color = _struct.unpack_from('<HH', data, offset)
        offset += 4
        text = _str.from_buffer(data, offset)
        offset += text.size

        item = MenuItems()
        item.model = model
        item.color = color
        item.text = text.value
        result.append(item)

    return result


_close_client_gump = _ScriptMethod(342)  # CloseClientGump
_close_client_gump.argtypes = [_uint]  # ID


def CloseClientGump(ID):
    _close_client_gump(ID)


_get_next_step_z = _ScriptMethod(366)  # GetNextStepZ
_get_next_step_z.restype = _byte
_get_next_step_z.argtypes = [_ushort,  # CurrX
                             _ushort,  # CurrY
                             _ushort,  # DestX
                             _ushort,  # DestY
                             _ubyte,  # WorldNum
                             _byte]  # CurrZ


def GetNextStepZ(CurrX, CurrY, DestX, DestY, WorldNum, CurrZ):
    return _get_next_step_z(CurrX, CurrY, DestX, DestY, WorldNum, CurrZ)


_client_hide = _ScriptMethod(368)  # ClientHide
_client_hide.restype = _bool
_client_hide.argtypes = [_uint]  # ID


def ClientHide(ID):
    return _client_hide(ID)


_get_skill_lock_state = _ScriptMethod(369)  # GetSkillLockState
_get_skill_lock_state.restype = _byte
_get_skill_lock_state.argtypes = [_str]  # SkillName


def GetSkillLockState(SkillName):
    return _get_skill_lock_state(SkillName)


_get_stat_lock_state = _ScriptMethod(372)  # GetStatLockState
_get_stat_lock_state.restype = _byte
_get_stat_lock_state.argtypes = [_str]  # SkillName


def GetStatLockState(SkillName):
    _get_stat_lock_state(SkillName)