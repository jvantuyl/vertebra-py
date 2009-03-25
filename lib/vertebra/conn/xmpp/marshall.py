"""Vertebra Marshaller for libxml2
   ===============================

   libxml2 only thinly wraps the C data structures. This can make it a bear to
   work with, as is apparent from this module.

   Extending the basic marshaller skeleton, we implement marshallers for most
   of the basic types. We extend the registry to automatically key
   unmarshalling from the XML tag type.

   Marshalling is a bit more complex. Since libxml wants to have C structures
   that all reference the same document object, we have to have a method to
   generate them. PyXMPP handles this with a StanzaPayloadObject. Using their
   hooks (the as_xml method), you can provide a few choice bits of information
   and they will call a method and let you build the XML object when it's
   actually used.

   As such, each marshaller embeds a simple class that provides this
   interface. The objects returned by the marshaller store the recursively
   (but partially) marshalled data, and they recursively build the object when
   PyXMPP realizes the stanzas to be delivered.

   Odd as it may seem, this appears to work fairly well and fairly quickly.
   This clearly shows that computers allow masochism at hitherto unseen
   speeds and efficiencies.
"""
from vertebra.marshall import *
from types import IntType,LongType,FloatType,StringTypes,DictType,ListType
from pyxmpp.objects import StanzaPayloadObject

# Namespace for Vertebra Elements
VERTEBRA_NS = 'http://xmlschema.engineyard.com/agent/api'

# Helper Generator that Iterates Children of a libxml2 XmlNode
def children(node):
  child = node.get_children()
  while child:
    yield child
    child = child.get_next()

# Marshall and Demarshall Integer Types
class INT(Marshaller):
  priority = 10
  
  class intr(StanzaPayloadObject):
    xml_element_name = 'int'
    xml_element_namespace = VERTEBRA_NS
    
    def __init__(self,data):
      self.data = str(data)
      
    def complete_xml_element(self,xmlnode,doc):
      xmlnode.setContent(self.data)
  
  @takes_types([IntType,LongType])
  def marshall(self,obj,marshall):
    return INT.intr(obj)

  @takes_keys(['int'])
  def unmarshall(self,obj,unmarshall):
    return int(obj.content)

# Marshall and Demarshall Floating Point Numbers
class FLOAT(Marshaller):
  priority = 10

  class fl(StanzaPayloadObject):
    xml_element_name = 'float'
    xml_element_namespace = VERTEBRA_NS

    def __init__(self,data): # for some reason, for floats,
      self.data = repr(data) # repr() seems to have more precision that str()

    def complete_xml_element(self,xmlnode,doc):
      xmlnode.setContent(self.data)

  @takes_types([FloatType])
  def marshall(self,obj,marshall):
    return FLOAT.fl(obj)

  @takes_keys(['float'])
  def unmarshall(self,obj,unmarshall):
    return float(obj.content)

# Marshall and Demarshall Unicode Strings
class STRING(Marshaller):
  priority = 10
  
  class st(StanzaPayloadObject):
    xml_element_name = 'string'
    xml_element_namespace = VERTEBRA_NS
    
    def __init__(self,data):
      self.data = str(data)
      
    def complete_xml_element(self,xmlnode,doc):
      xmlnode.setContent(self.data)
  
  @takes_types(StringTypes)
  def marshall(self,obj,marshall):
    return STRING.st(obj)
    
  @takes_keys('string')
  def unmarshall(self,obj,unmarshall):
    return obj.content

# Marshall and Demarshall Lists
class LIST(Marshaller):
  priority = 10

  class li(StanzaPayloadObject):
    xml_element_name = 'list'
    xml_element_namespace = VERTEBRA_NS

    def __init__(self,data):
      self.data = data

    def complete_xml_element(self,xmlnode,doc):
      for x in self.data:
        x.as_xml(parent=xmlnode,doc=doc)

  @takes_types([ListType])
  def marshall(self,obj,marshall):
    return LIST.li([marshall(x) for x in obj])

  @takes_keys('list')
  def unmarshall(self,obj,unmarshall):
    return [unmarshall(x) for x in children(obj)]

# Marshall and Demarshall Dictionaries
class DICT(Marshaller):
  priority = 10

  class di(StanzaPayloadObject):
    xml_element_name = 'struct'
    xml_element_namespace = VERTEBRA_NS

    def __init__(self,data):
      self.data = data

    def complete_xml_element(self,xmlnode,doc):
      for k,v in self.data.iteritems():
        n = v.as_xml(parent=xmlnode,doc=doc)
        n.setProp('key',str(k))

  @takes_types([DictType])
  def marshall(self,obj,marshall):
    return DICT.di(dict([(k,marshall(v),) for k,v in obj.iteritems()]))

  @takes_keys('struct')
  def unmarshall(self,obj,unmarshall):
    return dict([(x.prop("key"),unmarshall(x),) for x in children(obj)])

# Registry Class, Extended To Automatically Get Key From XML Tag
class XmlRegistry(Registry):
  def unmarshall(self,obj):
    return super(XmlRegistry,self).unmarshall(obj.get_name(),obj)

# Build Registry and Populate with Marshallers
registry = XmlRegistry()
registry.register(INT())
registry.register(FLOAT())
registry.register(STRING())
registry.register(LIST())
registry.register(DICT())
