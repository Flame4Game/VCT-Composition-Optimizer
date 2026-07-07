# VCT-Composition-Optimizer
A tool that assigns each agent of 5 in a composition to a VCT player, from the team provided, using log-scaled linear sum optimization.

## Instructions
1. Currently the only way to use this is by running it in your local code editor. I used VSC.
2. The instructions are straightforward but firstly you must import the players. I have given the option to use a team id from vlr.gg - most of the time it works but in some weird edge cases (6 active players, for example), it may be buggy. Otherwise you can simply input the player IDs manually, separated by spaces.
      Note you can actually add more than 5 players, it will calculate the optimal assignment out of the pool and cut out the unsuitable players.       This may be useful if you are looking at ENC rosters, for example.
3. Once player data is loaded (you may need to wait for a while), you must enter the comp. Any order will do, as long as there are no typos and the agent names are separated by spaces. (ex: jett sova kayo killjoy omen, Cypher Brimstone Tejo Breach Raze both work). There is also a preloaded dictionary of 8 varying comps if you want to try that first, simply enter d.
4. The assignments will appear in the console.

## Credits
Thank you to whoever made vlrdevapi, they are a godsend.
