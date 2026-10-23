"""Public profile portraits are enum-only mouse configurations, never uploads."""
CHOICES = {
    'fur': ('cream','silver','cocoa','charcoal','rose'),
    'hair': ('waves','bob','long','crop','bald','crew','swept'),
    'face': ('soft','square','rugged'),
    'facialHair': ('none','stubble','moustache','beard'),
    'hairColour': ('blonde','auburn','dark','silver','pink'),
    'build': ('slender','regular','broad','curvy','athletic'),
    'chest': ('flat','modest','full','voluptuous'),
    'outfit': ('jacket','dress','knit','shirt','leather'),
    'colour': ('navy','red','green','gold'),
    'accessory': ('none','pearls','glasses','bow'),
}
DEFAULT = dict(face='soft',facialHair='none',fur='cream',hair='waves',hairColour='blonde',build='regular',chest='modest',outfit='dress',colour='red',accessory='pearls')
def validate(value):
    if value is None:return dict(DEFAULT)
    if not isinstance(value,dict) or set(value)-set(CHOICES):raise ValueError('Choose a mouse avatar using the supplied options')
    result=dict(DEFAULT)
    for key,choice in value.items():
        if not isinstance(choice,str) or choice not in CHOICES[key]:raise ValueError('Choose a valid mouse '+key)
        result[key]=choice
    return result
