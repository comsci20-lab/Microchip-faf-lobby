from pathlib import Path
from lupa.lua51 import LuaRuntime
source=Path('data/fafengine/lua/ui/lobby/lobby.lua').read_text()
block=source[source.index('-- Ranked preferences'):source.index('local function ShowColourPreferences')]
lua=LuaRuntime()
lua.execute('''
Prefs={GetFromCurrentProfile=function() return nil end}
gameColors={PlayerColors={}}; for i=1,19 do gameColors.PlayerColors[i]=true end
GUI={uiCreated=true,slots={[1]={color={OnClick=function(self,c) gameInfo.PlayerOptions[1].PlayerColor=c; hostChanges=hostChanges+1 end}}}}
localPlayerID=10; hostID=20; requests={}; hostChanges=0; hosting=false
lobbyComm={IsHost=function() return hosting end,SendData=function(self,id,data) table.insert(requests,data.Color) end}
gameInfo={PlayerOptions={[1]={OwnerID=10,Human=true,PlayerColor=1},[2]={OwnerID=20,Human=true,PlayerColor=6}}}
gameInfo.PlayerOptions.pairs=function(self) local k=0;return function() k=k+1;if k<=2 then return k,self[k] end end end
FindSlotForID=function() return 1 end
UpdateGame=function() end; SetSlotInfo=function() end
''')
lua.execute(block+'\napply=ApplyPreferredColour; setPrefs=function(p) colourPrefs=p; colourAttempt=nil end')
for label,code in [
 ('occupied yellow falls back to blue', 'apply(); assert(requests[1]==11); assert(gameInfo.PlayerOptions[1].PlayerColor==1)'),
 ('no repeated requests before response', 'apply(); assert(#requests==1)'),
 ('fallback acknowledgement', 'gameInfo.PlayerOptions[1].PlayerColor=11; apply(); assert(#requests==1)'),
 ('yellow release requests immediately', 'gameInfo.PlayerOptions[2].PlayerColor=8; SetSlotInfo(); assert(requests[2]==6)'),
 ('rejection does not loop', 'apply(); assert(#requests==2)'),
 ('ready blocks switching', 'gameInfo.PlayerOptions[1].Ready=true; gameInfo.PlayerOptions[2].PlayerColor=3; apply(); assert(#requests==2)'),
 ('unready resumes', 'gameInfo.PlayerOptions[1].Ready=false; apply(); assert(requests[3]==6)'),
 ('organiser blocks switching', "ServerLobbyControl='organiser'; gameInfo.PlayerOptions[2].PlayerColor=4; apply(); assert(#requests==3); ServerLobbyControl=nil"),
 ('observer blocks switching','FindSlotForID=function() return nil end; apply(); assert(#requests==3); FindSlotForID=function() return 1 end'),
 ('host uses existing selector', 'hosting=true; apply(); assert(hostChanges==1); assert(gameInfo.PlayerOptions[1].PlayerColor==6)'),
 ('custom first preference', 'hosting=false; setPrefs({19,18,17}); apply(); assert(requests[4]==19)'),
 ('third preference when first two occupied', 'gameInfo.PlayerOptions[2].PlayerColor=19; gameInfo.PlayerOptions[3]={OwnerID=30,Human=false,PlayerColor=18}; gameInfo.PlayerOptions.pairs=function(self) local k=0; return function() k=k+1; if self[k] then return k,self[k] end end end; apply(); assert(requests[5]==17)'),
 ('all preferences occupied keeps current colour', 'gameInfo.PlayerOptions[4]={OwnerID=40,Human=true,PlayerColor=17}; apply(); assert(#requests==5); assert(gameInfo.PlayerOptions[1].PlayerColor==6)'),
 ('flat launch state ignored','gameInfo.PlayerOptions.pairs=nil; apply(); assert(hostChanges==1)')]:
 lua.execute(code);print('PASS',label)
# FAF uses generic table iteration; normalize only those existing lines for syntax validation.
normalized=source.replace('in GUI.slots do','in pairs(GUI.slots) do')
lua.execute('assert(loadstring(...))',normalized)
print('PASS complete hook Lua 5.1 syntax')
