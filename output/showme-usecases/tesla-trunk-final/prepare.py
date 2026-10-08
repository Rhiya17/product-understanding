from pathlib import Path
import json
from app.pipeline.authoring import Proposal,build_preview
from app.pipeline.fit_brief import build
root=Path('output/showme-usecases/tesla-trunk-final').resolve()
d=json.loads(Path('output/showme-usecases/tesla-exterior-correction/proposal.json').read_text())
s=d['python']
start=s.index('camera_poses = '); end=s.index('\nfor frame,loc,target in camera_poses:',start)
s=s[:start]+"camera_poses = [(1,(-6.8,-.14,1.65),(-.05,0,-.10)),(126,(-6.8,-.14,1.65),(-.05,0,-.10)),(164,(-4.75,-.06,1.65),(.17,0,.23)),(352,(-4.75,-.06,1.65),(.17,0,.23))]"+s[end:]
s=s.replace("ILLUSTRATIVE: 887 mm arch width - not verified.","Arch width unverified: 34.9 in (88.7 cm) illustrated.")
s=s.replace("'HUD_Unverified','Arch width unverified: 34.9 in (88.7 cm) illustrated.',-.343,-.171,.0200", "'HUD_Unverified','Arch width unverified: 34.9 in (88.7 cm) illustrated.',-.343,-.171,.0180")
a=s.index('caption_specs = ');b=s.index('\nfor i,(start,end,body_text)',a)
s=s[:a]+"caption_specs = [(1,32,'1  Folded: 31 x 20.5 x 11.5 in (78.7 x 52.1 x 29.2 cm)'),(33,48,'2  Hatch fully open. Lift the removable cargo cover.'),(49,88,'2  Remove the cover and set it aside before loading.'),(89,126,'3  Lift the folded stroller clear of the load floor.'),(127,178,'3  Lay flat, with its 31 in (78.7 cm) side across.'),(179,232,'3  Slide inward above the flush load lip.'),(233,278,'3  Lower to floor; leave 1 in (2.5 cm) at seatbacks.'),(279,326,'4  Close hatch. CUTAWAY: outer panels hidden.'),(327,352,'4  Closed cutaway: 11.5 in (29.2 cm) stroller height.')]"+s[b:]
s=s.replace("body_text,-.343,-.143,.0200", "body_text,-.343,-.143,.0180")
s=s.replace("panel(name+'_Panel',cx,cy,.181,.061)","panel(name+'_Panel',cx,cy,.200,.086)")
s=s.replace("hud_text(name+'_Value',line1,cx-.083,cy+.007,.0210)","hud_text(name+'_Value',line1.split('|')[0],cx-.093,cy+.022,.0220)")
s=s.replace("    objects.append(hud_text(name+'_Meaning',line2,cx-.083,cy-.020,.0200))", "    objects.append(hud_text(name+'_Metric',line1.split('|')[1],cx-.093,cy-.002,.0170))\n    objects.append(hud_text(name+'_Meaning',line2,cx-.093,cy-.027,.0180))")
s=s.replace("(.091 if toward>0 else -.091)","(.100 if toward>0 else -.100)")
s=s.replace("'1060 mm','floor depth',-.252,.085", "'41.7 in|(106 cm)','floor depth',-.246,.070")
s=s.replace("'1140 mm','opening',-.252,-.019", "'44.9 in|(114 cm)','opening',-.246,-.029")
s=s.replace("'680 mm','height limit',.252,.085", "'26.8 in|(68 cm)','height limit',.246,.070")
s=s.replace("'292.1 mm','stroller tall',.252,-.019", "'11.5 in|(29.2 cm)','stroller height',.246,-.029")
d['python']=s
d['notes']='User approved trunk-focused video with inches first, centimeters second; final render authorized after updated preview inspection.'
(root/'proposal.json').write_text(json.dumps(d,indent=2))
fit=build('graco-ready2jet-2212125','tesla-model-y');(root/'fit.json').write_text(json.dumps(fit,indent=2));print(build_preview(Proposal.model_validate(d),root/'preview',fit_checks=fit['checks']))
