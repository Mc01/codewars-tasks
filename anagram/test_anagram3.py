import time
from decimal import Decimal

from anagram_akcelero import listPosition

word = "ll5555XIPAfQDDDDDDDDDDDmQBAEEEEEEEEEEEElT3AOljoXlQPownaZ6s777777777777777DtG7777EgUUUUUUUUUUUUUhBV8fWGQttttttttthUGGGGGGGGGGGGGGMob8d8DNNDcccccccccccccIQQQQQQQQQQQQzIIIEEVVVVVVVVVVPnAm5clNF0LHHHHHHHHHHHHHHyyyyyySnB8rJNcvx9EEEEEEEEEE85CfffffffffffffWKwg2lx8bbbbbbbbbbbwmD04EzKiYDxIjmj55555555555555es5qqqq5rSS888888888888p2q70RGWa2IkWWWWWWWWWWWW5uUUUUUUWyTY9zPITVBAuuuuuurhmT4ijWWWPD4NNNNNNNNNNNNNNNJ1222222222VVVVVVyJcmXE4XhhhhhhhhhhhhheN4UXXXXXXXrmmmmmmmmmmm77ROSmmlcJ0111111111111BBBBBBBBBBBBBoikllllllll7nTaY0kSnhdTLDGwwwwwwwwwDgNFNrbWWWOOOOOOOOOOOOk6666666WzI3vh0wyFFFFFFFFFFF00000000000000Y555555555555YoSk8444444444440AmoR1bYoO6n7ol9LVOKB7qzZOxjmSsWtrvTyXXXXXXXXXXippppppppVVVVVVVVVVVVViiiiiiiiDDDDDDXZiiiiiiiiiiiiLPxUP8InmspmqUSwwwwwwwwwwwwwwwiGzhhhhhhhhh65lgfaaaaOOOOOOOOOOIGqNiQSNqMqxJ8bXXXGsCoLaJ53OH333333334jAVf9Y8EEEEEEEEEEEE8KVnXQ9vLAmIIIIIIIIIIIIIITR33333uRRRufGDth2RRRRRRRRRRRRBdDCCCCCC6aaaaaaaaaaQzC5YRaaaaaxENqZRRYFRfOSSSKrmeSQp4YTIVVVVVVVVVVVVBwZ87iq2P1ylVtSKo4uOfbUplFc7lllbwiiiii"

start = Decimal(str(time.time()))
listPosition(word)
stop = Decimal(str(time.time()))

print(stop - start)
