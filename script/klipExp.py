# coding=utf-8
import klip

DATA = """The Three-Body Problem (Cixin Liu)
- Highlight on Page 42 | Loc. 631-32  | Added on Monday, May 15, 2017, 11:14 PM

Ye saw the words TRANSMISSION MAIN CONTROL ROOM"""

DATA2 = """Surfing Uncertainty: Prediction, Action, and the Embodied Mind (Clark, Andy)
- Your Highlight on page 70 | Location 1613-1616 | Added on Wednesday, April 13, 2016 10:39:18 PM

The only hypothesis that can endure over successive saccades is the one that correctly predicts the salient features that are sampled. … This means that the hypothesis prescribes its own verification and can only survive if it is a correct representation of the world. If its salient features are not discovered, it will be discarded in favor of a better hypothesis. (Friston, Adams, et al., 2012, p. 16)"""

DATA3 = """Regular Expressions Cookbook (Jan Goyvaerts and Steven Levithan)
- Your Note on Page 41 | Location 391 | Added on Wednesday, November 27, 2013 10:52:55 AM

regex should not be allowed"""


def run():
    parsed = klip.load(DATA3, "Touch")
    print parsed[0]["added_on"]


if __name__ == '__main__':
    run()
