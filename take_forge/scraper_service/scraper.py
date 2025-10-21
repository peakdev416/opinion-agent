class Scraper:
    def __init__(self):
        self._articles: list[dict] = [
            {
                "id": "art001",
                "title": "Kyrie Irving’s Return Signals a Turning Point for the Mavericks",
                "published_at": "2025-10-16",
                "source_url": "https://sportsdemo.com/articles/kyrie-irving-return",
                "content": (
                    "After missing the last six weeks due to a hamstring strain, Kyrie Irving returned to full practice with the Dallas Mavericks on Tuesday, and all signs point to him suiting up for Friday night’s home game. "
                    "The Mavericks, who went 4–8 in his absence, have clearly missed his presence on both ends of the floor. Without his shot creation and perimeter playmaking, Luka Doncic has been forced to shoulder a heavier load, resulting in increased fatigue and a visible drop in late-game execution. "
                    "Irving’s return is not just about scoring—it’s about floor spacing, off-ball movement, and defensive pressure on opposing guards. His ability to read defensive switches and create mismatches has been sorely missed by the Mavs’ coaching staff. "
                    "Coach Jason Kidd said, 'Having Kyrie back opens up so much for our offense. Guys like Tim [Hardaway Jr.] and Grant [Williams] will see better looks, and Luka won’t have to do everything on every possession.' "
                    "With the Mavs currently sitting at the 8th seed, this next stretch could define their season. A healthy Irving may be the catalyst that pushes them back into the top 5 conversation in the Western Conference."
                ),
            },
            {
                "id": "art002",
                "title": "Steph Curry Adjusts Game to Support Warriors' Younger Core",
                "published_at": "2025-10-10",
                "source_url": "https://sportsdemo.com/articles/curry-leadership-2025",
                "content": (
                    "Entering his 17th NBA season, Stephen Curry isn’t slowing down—but he is adapting. After a summer focused on strength, mobility, and recovery, Curry arrived at training camp visibly leaner and more focused on off-ball facilitation. "
                    "With rising players like Jonathan Kuminga and Moses Moody stepping into larger roles, Curry has emphasized ball movement and leadership over volume shooting. "
                    "In preseason action, Curry has averaged just 12 points per game—but his assist numbers are up, and the Warriors' offensive flow has looked more cohesive than it did last season. "
                    "'I don’t need to be the guy who drops 30 every night,' Curry told reporters. 'I’m more focused on creating space, trusting our younger guys, and helping them get comfortable in the system.' "
                    "Steve Kerr echoed the sentiment, noting that Curry’s presence alone changes the gravity of the court. 'Even when he doesn’t touch the ball, he’s shaping the defense. That’s elite leadership in action.' "
                    "With Klay Thompson on a minutes restriction and Draymond Green out for the first two weeks, the Warriors will need Curry’s veteran stability more than ever."
                ),
            },
            {
                "id": "art003",
                "title": "Victor Wembanyama’s Sophomore Leap Is Already Taking Shape",
                "published_at": "2025-10-05",
                "source_url": "https://sportsdemo.com/articles/wemby-sophomore-season",
                "content": (
                    "San Antonio’s Victor Wembanyama made waves in his rookie season with jaw-dropping blocks, highlight dunks, and guard-like ball handling. But it’s the early signs in year two that suggest he’s evolving into a true franchise cornerstone. "
                    "Through the Spurs’ first five games, Wembanyama is averaging 22.4 points, 9.1 rebounds, and 3.7 blocks per game—all while playing under 30 minutes. "
                    "The most noticeable difference? Poise. The 7’4” phenom is no longer rushing shots or biting on pump fakes. His footwork has improved, and he’s beginning to control games from the defensive end out. "
                    "Popovich has given him more freedom offensively as well, using him in high pick-and-rolls, trail threes, and even post-isolation sets. "
                    "‘He’s figuring it out faster than we expected,’ assistant coach Mitch Johnson said. ‘What’s scary is that he hasn’t even unlocked his full offensive bag yet.’ "
                    "If Wemby’s trajectory continues, San Antonio may not be in the lottery much longer."
                ),
            },
            {
                "id": "art004",
                "title": "Are the Celtics Built for a Championship Run or Another Collapse?",
                "published_at": "2025-10-12",
                "source_url": "https://sportsdemo.com/articles/celtics-2025-analysis",
                "content": (
                    "After yet another deep playoff run ended in heartbreak, the Boston Celtics retooled their roster with a clear objective: get over the hump. But whether the pieces fit remains to be seen. "
                    "The acquisition of Jrue Holiday adds defensive tenacity and veteran poise, while Kristaps Porzingis brings scoring versatility from the frontcourt. On paper, it’s a title-caliber team. "
                    "But the question persists: Can Jayson Tatum and Jaylen Brown coexist as true co-alphas? In moments of adversity, their chemistry has sometimes faltered, and crunch-time decision making has been inconsistent. "
                    "Coach Joe Mazzulla has emphasized ball movement and defensive identity in camp, but those philosophies will be stress-tested in close games. "
                    "‘We’ve got everything we need,’ Tatum said. ‘Now it’s about putting it together when it matters.’ "
                    "The East is wide open, but if Boston falters again, changes could come quicker than expected."
                ),
            },
            {
                "id": "art005",
                "title": "Can Zion Williamson Finally Deliver a Full Season for the Pelicans?",
                "published_at": "2025-10-09",
                "source_url": "https://sportsdemo.com/articles/zion-season-preview",
                "content": (
                    "There may not be a more polarizing figure in the NBA than Zion Williamson. When healthy, he’s unstoppable—an explosive mix of power, agility, and touch. "
                    "But over four seasons, injuries have limited him to just 114 total games. This year, Williamson is aiming to change that narrative. "
                    "Reports out of Pelicans camp suggest that Zion has dropped 15 pounds and focused on core stability and flexibility during the offseason. "
                    "New Orleans is taking a cautious approach—no back-to-backs for the first month and managed minutes early. "
                    "‘Zion is in a great place mentally and physically,’ said head coach Willie Green. ‘We’re not rushing anything. The goal is sustained impact.’ "
                    "With Brandon Ingram healthy, CJ McCollum in rhythm, and a deep supporting cast, the Pelicans could make noise—if Zion stays upright. "
                    "The talent has never been the question. It’s all about durability now."
                ),
            },
        ]
        self._idx = 0

    def next_article(self) -> dict | None:
        if self._idx >= len(self._articles):
            self._idx = 0  # or return None to stop; your call
        art = self._articles[self._idx]
        self._idx += 1
        return art
