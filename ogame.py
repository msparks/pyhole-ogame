import locale
import math
import re
import urllib

from pyhole import plugin
from pyhole import utils


class Cost(object):
  def __init__(self, metal, crystal, deuterium):
    self._metal = metal
    self._crystal = crystal
    self._deuterium = deuterium

  def __add__(self, other):
    return Cost(self._metal + other.metal,
                self._crystal + other.crystal,
                self._deuterium + other.deuterium)

  @property
  def metal(self):
    return self._metal

  @property
  def crystal(self):
    return self._crystal

  @property
  def deuterium(self):
    return self._deuterium


class Entity(object):
  def __init__(self, name, cost=None):
    self._name = name
    self._cost = cost

  @property
  def name(self):
    return self._name

  @property
  def cost(self):
    return self._cost


class Facility(Entity):
  def __init__(self, name, cost, min_robotics_level):
    Entity.__init__(self, name, cost)
    self._min_robotics_level = min_robotics_level


class Ship(Entity):
  def __init__(self, name, cost, min_shipyard_level):
    Entity.__init__(self, name, cost)
    self._min_shipyard_level = min_shipyard_level


class Defense(Entity):
  def __init__(self, name, cost, min_shipyard_level):
    Entity.__init__(self, name, cost)
    self._min_shipyard_level = min_shipyard_level


class Technology(Entity):
  def __init__(self, name, cost, min_research_level):
    Entity.__init__(self, name, cost)
    self._min_research_level = min_research_level


class MetalMine(Facility):
  def __init__(self):
    Facility.__init__(self, 'Metal Mine', Cost(60, 15, 0), 0)

class CrystalMine(Facility):
  def __init__(self):
    Facility.__init__(self, 'Crystal Mine', Cost(48, 24, 0), 0)

class DeuteriumSynthesizer(Facility):
  def __init__(self):
    Facility.__init__(self, 'Deuterium Synthesizer', Cost(225, 75, 0), 0)

class SolarPlant(Facility):
  def __init__(self):
    Facility.__init__(self, 'Solar Plant', Cost(75, 30, 0), 0)

class FusionReactor(Facility):
  def __init__(self):
    Facility.__init__(self, 'Fusion Reactor', Cost(900, 360, 180), 0)

class RoboticsFactory(Facility):
  def __init__(self):
    Facility.__init__(self, 'Robotics Factory', Cost(400, 120, 200), 0)

class NaniteFactory(Facility):
  def __init__(self):
    Facility.__init__(
        self, 'Nanite Factory', Cost(1000000, 500000, 100000), 10)

class Shipyard(Facility):
  def __init__(self):
    Facility.__init__(self, 'Shipyard', Cost(400, 200, 100), 2)

class MetalStorage(Facility):
  def __init__(self):
    Facility.__init__(self, 'Metal Storage', Cost(2000, 0, 0), 0)

class CrystalStorage(Facility):
  def __init__(self):
    Facility.__init__(self, 'Crystal Storage', Cost(2000, 1000, 0), 0)

class DeuteriumTank(Facility):
  def __init__(self):
    Facility.__init__(self, 'Deuterium Tank', Cost(2000, 2000, 0), 0)

class ResearchLab(Facility):
  def __init__(self):
    Facility.__init__(self, 'Research Lab', Cost(200, 400, 200), 0)

class RocketSilo(Facility):
  def __init__(self):
    Facility.__init__(self, 'Rocket Silo', Cost(20000, 20000, 0), 0)

class LunarBase(Facility):
  def __init__(self):
    Facility.__init__(self, 'Lunar Base', Cost(20000, 40000, 20000), 0)

class SensorPhalanx(Facility):
  def __init__(self):
    Facility.__init__(self, 'Sensor Phalanx', Cost(20000, 40000, 20000), 0)

class JumpGate(Facility):
  def __init__(self):
    Facility.__init__(self, 'Jump Gate', Cost(2000000, 4000000, 2000000), 0)

class EspionageTechnology(Technology):
  def __init__(self):
    Technology.__init__(self, 'Espionage Technology', Cost(200, 1000, 200), 3)

class ComputerTechnology(Technology):
  def __init__(self):
    Technology.__init__(self, 'Computer Technology', Cost(0, 400, 600), 1)

class WeaponsTechnology(Technology):
  def __init__(self):
    Technology.__init__(self, 'Weapons Technology', Cost(800, 200, 0), 4)

class ShieldingTechnology(Technology):
  def __init__(self):
    Technology.__init__(self, 'Shielding Technology', Cost(200, 600, 0), 6)

class ArmorTechnology(Technology):
  def __init__(self):
    Technology.__init__(self, 'Armor Technology', Cost(1000, 0, 0), 2)

class EnergyTechnology(Technology):
  def __init__(self):
    Technology.__init__(self, 'Energy Technology', Cost(0, 800, 400), 1)

class HyperspaceTechnology(Technology):
  def __init__(self):
    Technology.__init__(self, 'Hyperspace Technology', Cost(0, 4000, 2000), 7)

class CombustionDrive(Technology):
  def __init__(self):
    Technology.__init__(self, 'Combustion Drive', Cost(400, 0, 600), 1)

class ImpulseDrive(Technology):
  def __init__(self):
    Technology.__init__(self, 'Impulse Drive', Cost(2000, 4000, 600), 2)

class HyperspaceDrive(Technology):
  def __init__(self):
    Technology.__init__(
        self, 'Hyperspace Drive', Cost(10000, 20000, 6000), 7)

class LaserTechnology(Technology):
  def __init__(self):
    Technology.__init__(self, 'Laser Technology', Cost(200, 100, 0), 1)

class IonTechnology(Technology):
  def __init__(self):
    Technology.__init__(self, 'Ion Technology', Cost(1000, 300, 100), 4)

class PlasmaTechnology(Technology):
  def __init__(self):
    Technology.__init__(self, 'Plasma Technology', Cost(2000, 4000, 1000), 4)

class ResearchNetwork(Technology):
  def __init__(self):
    Technology.__init__(
        self, 'Research Network', Cost(240000, 400000, 160000), 10)

class SmallCargo(Ship):
  def __init__(self):
    Ship.__init__(self, 'Small Cargo', Cost(2000, 2000, 0), 2)

class LargeCargo(Ship):
  def __init__(self):
    Ship.__init__(self, 'Large Cargo', Cost(6000, 6000, 0), 4)

class LightFighter(Ship):
  def __init__(self):
    Ship.__init__(self, 'Light Fighter', Cost(3000, 1000, 0), 1)

class HeavyFighter(Ship):
  def __init__(self):
    Ship.__init__(self, 'Heavy Fighter', Cost(6000, 4000, 0), 3)

class Cruiser(Ship):
  def __init__(self):
    Ship.__init__(self, 'Cruiser', Cost(20000, 7000, 2000), 5)

class Battleship(Ship):
  def __init__(self):
    Ship.__init__(self, 'Battleship', Cost(40000, 20000, 0), 7)

class ColonyShip(Ship):
  def __init__(self):
    Ship.__init__(self, 'Colony Ship', Cost(10000, 20000, 10000), 4)

class Recycler(Ship):
  def __init__(self):
    Ship.__init__(self, 'Recycler', Cost(10000, 6000, 2000), 4)

class EspionageProbe(Ship):
  def __init__(self):
    Ship.__init__(self, 'Espionage Probe', Cost(0, 1000, 0), 3)

class Bomber(Ship):
  def __init__(self):
    Ship.__init__(self, 'Bomber', Cost(50000, 25000, 15000), 8)

class SolarSatellite(Ship):
  def __init__(self):
    Ship.__init__(self, 'Solar Satellite', Cost(0, 2000, 500), 1)

class Destroyer(Ship):
  def __init__(self):
    Ship.__init__(self, 'Destroyer', Cost(60000, 50000, 15000), 9)

class DeathStar(Ship):
  def __init__(self):
    Ship.__init__(self, 'Death Star', Cost(5000000, 4000000, 1000000), 12)

class MissileLauncher(Defense):
  def __init__(self):
    Defense.__init__(self, 'Missile Launcher', Cost(2000, 0, 0), 1)

class SmallLaser(Defense):
  def __init__(self):
    Defense.__init__(self, 'Small Laser', Cost(1500, 500, 0), 2)

class HeavyLaser(Defense):
  def __init__(self):
    Defense.__init__(self, 'Heavy Laser', Cost(6000, 2000, 0), 4)

class GaussCannon(Defense):
  def __init__(self):
    Defense.__init__(self, 'Gauss Cannon', Cost(20000, 15000, 2000), 6)

class IonCannon(Defense):
  def __init__(self):
    Defense.__init__(self, 'Ion Cannon', Cost(2000, 6000, 0), 4)

class PlasmaCannon(Defense):
  def __init__(self):
    Defense.__init__(self, 'Plasma Cannon', Cost(50000, 50000, 30000), 8)

class SmallShieldDome(Defense):
  def __init__(self):
    Defense.__init__(self, 'Small Shield Dome', Cost(10000, 10000, 0), 1)

class LargeShieldDome(Defense):
  def __init__(self):
    Defense.__init__(self, 'Large Shield Dome', Cost(50000, 50000, 0), 6)

class AntiBallisticMissile(Defense):
  def __init__(self):
    Defense.__init__(self, 'Anti-Ballistic Missile', Cost(8000, 0, 2000), 0)

class InterplanetaryMissile(Defense):
  def __init__(self):
    Defense.__init__(
        self, 'Interplanetary Missile', Cost(12500, 2500, 10000), 0)


def build_cost(entity, level):
  metal = 0
  crystal = 0
  deuterium = 0

  if type(entity) == MetalMine:
    metal = 60 * (1.5 ** (level - 1))
    crystal = 15 * (1.5 ** (level - 1))
  elif type(entity) == CrystalMine:
    metal = 48 * (1.6 ** (level - 1))
    crystal = 24 * (1.6 ** (level - 1))
  elif type(entity) == DeuteriumSynthesizer:
    metal = 225 * (1.5 ** (level - 1))
    crystal = 75 * (1.5 ** (level - 1))
  elif type(entity) == SolarPlant:
    metal = 75 * (1.5 ** (level - 1))
    crystal = 30 * (1.5 ** (level - 1))
  elif type(entity) == FusionReactor:
    metal = 900 * (1.8 ** (level - 1))
    crystal = 360 * (1.8 ** (level - 1))
    deuterium = 180 * (1.8 ** (level - 1))
  else:
    metal = entity.cost.metal * (2 ** (level - 1))
    crystal = entity.cost.crystal * (2 ** (level - 1))
    deuterium = entity.cost.deuterium * (2 ** (level - 1))

  return Cost(int(math.floor(metal)),
              int(math.floor(crystal)),
              int(math.floor(deuterium)))

def entity_map():
  entities = {
      'metal': MetalMine(),
      'crystal': CrystalMine(),
      'deuterium': DeuteriumSynthesizer(),
      'solar': SolarPlant(),
      'fusion': FusionReactor(),
      'robot': RoboticsFactory(),
      'robotics': RoboticsFactory(),
      'nanite': NaniteFactory(),
      'nanites': NaniteFactory(),
      'shipyard': Shipyard(),
      'mstorage': MetalStorage(),
      'cstorage': CrystalStorage(),
      'dtank': DeuteriumTank(),
      'lab': ResearchLab(),
      'silo': RocketSilo(),
      'lunar': LunarBase(),
      'phalanx': SensorPhalanx(),
      'jump': JumpGate(),
      'espionage': EspionageTechnology(),
      'computer': ComputerTechnology(),
      'weapon': WeaponsTechnology(),
      'shielding': ShieldingTechnology(),
      'armour': ArmorTechnology(),
      'armor': ArmorTechnology(),
      'energy': EnergyTechnology(),
      'hyperspace': HyperspaceTechnology(),
      'combustion': CombustionDrive(),
      'impulse': ImpulseDrive(),
      'hyperdrive': HyperspaceDrive(),
      'laser': LaserTechnology(),
      'iontech': IonTechnology(),
      'plasmatech': PlasmaTechnology(),
      'network': ResearchNetwork(),
      'scargo': SmallCargo(),
      'lcargo': LargeCargo(),
      'lfighter': LightFighter(),
      'hfighter': HeavyFighter(),
      'cruiser': Cruiser(),
      'bship': Battleship(),
      'colony': ColonyShip(),
      'recycler': Recycler(),
      'probe': EspionageProbe(),
      'bomber': Bomber(),
      'sat': SolarSatellite(),
      'destroyer': Destroyer(),
      'rip': DeathStar(),
      'missile': MissileLauncher(),
      'slaser': SmallLaser(),
      'hlaser': HeavyLaser(),
      'gauss': GaussCannon(),
      'ion': IonCannon(),
      'plasma': PlasmaCannon(),
      'sdome': SmallShieldDome(),
      'ldome': LargeShieldDome(),
      'abm': AntiBallisticMissile(),
      'ipm': InterplanetaryMissile()
  }
  return entities


def entity_from_alias(alias):
  entities = entity_map()
  if alias in entities:
    return entities[alias]
  return None


def format_number(n, format='%d'):
  locale.setlocale(locale.LC_ALL, '')
  return locale.format(format, n, grouping=True)


class Ogame(plugin.Plugin):
  """Ogame calculations."""

  @plugin.hook_add_command('cost')
  def cost(self, params=None, **kwargs):
    """Calculate build cost of an entity."""
    if params is None:
      params = ''
    m = re.match(r'\s*([a-z]+)\s+(?:(\d+) to\s+)?(\d+)', params)
    if not m:
      self.irc.reply('Syntax: .cost <entity> [<start level> to] <end level>')
      return

    alias, start_level, end_level = m.groups()
    end_level = int(end_level)
    if start_level is None:
      start_level = end_level - 1
    else:
      start_level = int(start_level)

    entity = entity_from_alias(alias)
    if entity is None:
      self.irc.reply('Unknown entity: %s' % alias)
      return
    if end_level < 1:
      self.irc.reply('End level must be greater than 0.')
      return
    if end_level < start_level:
      self.irc.level('End level must be larger than start level.')
      return

    cost = Cost(0, 0, 0)
    for l in range(start_level, end_level + 1):
      cost += build_cost(entity, l)

    self.irc.reply('%s level %s to %s: %s metal, %s crystal, %s deuterium.' %
                   (entity.name, start_level, end_level,
                    format_number(cost.metal),
                    format_number(cost.crystal),
                    format_number(cost.deuterium)))

  @plugin.hook_add_command('entities')
  def entities(self, params=None, **kwargs):
    """Sends a list of entity aliases to the user."""
    entities = entity_map()

    # Sort entities into type => <set of aliases>.
    type_to_aliases = {}
    for alias in entities:
      entity = entities[alias]

      if isinstance(entity, Facility):
        type_name = 'Facilities'
      elif isinstance(entity, Ship):
        type_name = 'Ships'
      elif isinstance(entity, Defense):
        type_name = 'Defense'
      elif isinstance(entity, Technology):
        type_name = 'Technology'

      if type_name not in type_to_aliases:
        type_to_aliases[type_name] = set()
      type_to_aliases[type_name].add(alias)

    nick = self.irc.source.split('!')[0]
    self.irc.reply('Sending list of entities to %s.' % nick)

    for type_name in type_to_aliases:
      aliases = sorted(list(type_to_aliases[type_name]))
      self.irc.privmsg(nick, '%s: %s' % (type_name, ', '.join(aliases)))
