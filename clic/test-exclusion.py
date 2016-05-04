#!/bin/env python

import os, sys

import cheshire3
from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.internal import cheshire3Root
from cheshire3.document import StringDocument

from lxml import etree

# Launch a Cheshire session
session = Session()
serverConfig = os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
serv = SimpleServer(session, serverConfig)

# Grab our objects
db = serv.get_object(session, 'db_dickens')
xmlp = db.get_object(session, 'LxmlParser')
excl = db.get_object(session, 'quoteExcludeSpanSelector')

if '--exclude' in sys.argv:
    
    data = """<div>
<p type="speech" id="BH.c6.p114">
            <s id="BH.c6.s340">
                          <qs/>
                                    "My dear Miss Summerson,"
                          <qe/>
                          said Richard in a whisper,
                          <qs/>
                                    "I have ten pounds that I received from Mr. Kenge.
            </s>
            <s id="BH.c6.s341">
                                    I must try what that will do."
                          <qe/>
                          Richard is a bit of a weird guy. 
            </s>
            #IGNORED But this is ignored, somehow?
</p>
<p type="speech" id="BH.c6.p114">
            <s id="BH.c6.s340">
                          <qs/>
                                    "My dear Miss Summerson,"
                          <qe/>
                          said blabla in a whisper,
                          <qs/>
                                    "I have ten pounds that I received from Mr. Kenge.
            </s>
            <s id="BH.c6.s341">
                                    I must try what that will do."
                          <qe/>
                          Blabla is a bit of a weird guy. 
            </s>
            # IGNORED But this is ignored, somehow?
</p>
</div>
"""

    doc = StringDocument(data)
    rec = xmlp.process_document(session, doc)
    res = excl.process_record(session, rec)
    print etree.tostring(res[0])




if '--exclude-long' in sys.argv:
        
    data = '''
    <div>

    <p pid="64" id="arma.c3.p64"><s sid="177" id="arma.c3.s177">It was close on one o'clock, and the bell was ringing which summoned the visitors to their early dinner at the inn.</s> <s sid="178" id="arma.c3.s178">The quick beat of footsteps, and the gathering hum of voices outside, penetrated gayly into the room, as Mr. Neal spread the manuscript before him on the table, and read the opening sentences in these words:</s> </p>

    <p pid="65" id="arma.c3.p65" type="speech" form="extended" position="beginning"><s sid="179" id="arma.c3.s179"><qs/>"I address this letter to my son, when my son is of an age to understand it.</s> <s sid="180" id="arma.c3.s180">Having lost all hope of living to see my boy grow up to manhood, I have no choice but to write here what I would fain have said to him at a future time with my own lips.</s> </p><p pid="66" id="arma.c3.p66" type="speech" form="extended" position="middle"><s sid="181" id="arma.c3.s181">"I have three objects in writing.</s> <s sid="182" id="arma.c3.s182">First, to reveal the circumstances which attended the marriage of an English lady of my acquaintance, in the island of Madeira.</s> <s sid="183" id="arma.c3.s183">Secondly, to throw the true light on the death of her husband a short time afterward, on board the French timber ship _La Grace de Dieu_.</s> <s sid="184" id="arma.c3.s184">Thirdly, to warn my son of a danger that lies in wait for him--a danger that will rise from his father's grave when the earth has closed over his father's ashes.</s> </p>

    <p pid="67" id="arma.c3.p67" type="speech" form="extended" position="middle"><s sid="185" id="arma.c3.s185">"The story of the English lady's marriage begins with my inheriting the great Armadale property, and my taking the fatal Armadale name.</s> </p>

    <p pid="68" id="arma.c3.p68" type="speech" form="extended" position="middle"><s sid="186" id="arma.c3.s186">"I am the only surviving son of the late Mathew Wrentmore, of Barbadoes.</s> <s sid="187" id="arma.c3.s187">I was born on our family estate in that island, and I lost my father when I was still a child.</s> <s sid="188" id="arma.c3.s188">My mother was blindly fond of me; she denied me nothing, she let me live as I pleased.</s> <s sid="189" id="arma.c3.s189">My boyhood and youth were passed in idleness and self-indulgence, among people--slaves and half-castes mostly--to whom my will was law.</s> <s sid="190" id="arma.c3.s190">I doubt if there is a gentleman of my birth and station in all England as ignorant as I am at this moment.</s> <s sid="191" id="arma.c3.s191">I doubt if there was ever a young man in this world whose passions were left so entirely without control of any kind as mine were in those early days.</s> </p>

    <p pid="69" id="arma.c3.p69" type="speech" form="extended" position="middle"><s sid="192" id="arma.c3.s192">"My mother had a woman's romantic objection to my father's homely Christian name.</s> <s sid="193" id="arma.c3.s193">I was christened Allan, after the name of a wealthy cousin of my father's--the late Allan Armadale--who possessed estates in our neighborhood, the largest and most productive in the island, and who consented to be my godfather by proxy.</s> <s sid="194" id="arma.c3.s194">Mr. Armadale had never seen his West Indian property.</s> <s sid="195" id="arma.c3.s195">He lived in England; and, after sending me the customary godfather's present, he held no further communication with my parents for years afterward.</s> <s sid="196" id="arma.c3.s196">I was just twenty-one before we heard again from Mr. Armadale.</s> <s sid="197" id="arma.c3.s197">On that occasion my mother received a letter from him asking if I was still alive, and offering no less (if I was) than to make me the heir to his West Indian property.</s> </p>

    <p pid="70" id="arma.c3.p70" type="speech" form="extended" position="middle"><s sid="198" id="arma.c3.s198">"This piece of good fortune fell to me entirely through the misconduct of Mr. Armadale's son, an only child.</s> <s sid="199" id="arma.c3.s199">The young man had disgraced himself beyond all redemption; had left his home an outlaw; and had been thereupon renounced by his father at once and forever.</s> <s sid="200" id="arma.c3.s200">Having no other near male relative to succeed him, Mr. Armadale thought of his cousin's son and his own godson; and he offered the West Indian estate to me, and my heirs after me, on one condition--that I and my heirs should take his name.</s> <s sid="201" id="arma.c3.s201">The proposal was gratefully accepted, and the proper legal measures were adopted for changing my name in the colony and in the mother country.</s> <s sid="202" id="arma.c3.s202">By the next mail information reached Mr. Armadale that his condition had been complied with.</s> <s sid="203" id="arma.c3.s203">The return mail brought news from the lawyers.</s> <s sid="204" id="arma.c3.s204">The will had been altered in my favor, and in a week afterward the death of my benefactor had made me the largest proprietor and the richest man in Barbadoes.</s> </p>

    <p pid="71" id="arma.c3.p71" type="speech" form="extended" position="middle"><s sid="205" id="arma.c3.s205">"This was the first event in the chain.</s> <s sid="206" id="arma.c3.s206">The second event followed it six weeks afterward.</s> </p>

    <p pid="72" id="arma.c3.p72" type="speech" form="extended" position="middle"><s sid="207" id="arma.c3.s207">"At that time there happened to be a vacancy in the clerk's office on the estate, and there came to fill it a young man about my own age who had recently arrived in the island.</s> <s sid="208" id="arma.c3.s208">He announced himself by the name of Fergus Ingleby.</s> <s sid="209" id="arma.c3.s209">My impulses governed me in everything; I knew no law but the law of my own caprice, and I took a fancy to the stranger the moment I set eyes on him.</s> <s sid="210" id="arma.c3.s210">He had the manners of a gentleman, and he possessed the most attractive social qualities which, in my small experience, I had ever met with.</s> <s sid="211" id="arma.c3.s211">When I heard that the written references to character which he had brought with him were pronounced to be unsatisfactory, I interfered, and insisted that he should have the place.</s> <s sid="212" id="arma.c3.s212">My will was law, and he had it.</s> </p>

    <p pid="73" id="arma.c3.p73" type="speech" form="extended" position="middle"><s sid="213" id="arma.c3.s213">"My mother disliked and distrusted Ingleby from the first.</s> <s sid="214" id="arma.c3.s214">When she found the intimacy between us rapidly ripening; when she found me admitting this inferior to the closest companionship and confidence (I had lived with my inferiors all my life, and I liked it), she made effort after effort to part us, and failed in one and all.</s> <s sid="215" id="arma.c3.s215">Driven to her last resources, she resolved to try the one chance left--the chance of persuading me to take a voyage which I had often thought of--a voyage to England.</s> </p>

    <p pid="74" id="arma.c3.p74" type="speech" form="extended" position="middle"><s sid="216" id="arma.c3.s216">"Before she spoke to me on the subject, she resolved to interest me in the idea of seeing England, as I had never been interested yet.</s> <s sid="217" id="arma.c3.s217">She wrote to an old friend and an old admirer of hers, the late Stephen Blanchard, of Thorpe Ambrose, in Norfolk--a gentleman of landed estate, and a widower with a grown-up family.</s> <s sid="218" id="arma.c3.s218">After-discoveries informed me that she must have alluded to their former attachment (which was checked, I believe, by the parents on either side); and that, in asking Mr. Blanchard's welcome for her son when he came to England, she made inquiries about his daughter, which hinted at the chance of a marriage uniting the two families, if the young lady and I met and liked one another.</s> <s sid="219" id="arma.c3.s219">We were equally matched in every respect, and my mother's recollection of her girlish attachment to Mr. Blanchard made the prospect of my marrying her old admirer's daughter the brightest and happiest prospect that her eyes could see.</s> <s sid="220" id="arma.c3.s220">Of all this I knew nothing until Mr. Blanchard's answer arrived at Barbadoes.</s> <s sid="221" id="arma.c3.s221">Then my mother showed me the letter, and put the temptation which was to separate me from Fergus Ingleby openly in my way.</s> </p>

    <p pid="75" id="arma.c3.p75" type="speech" form="extended" position="middle"><s sid="222" id="arma.c3.s222">"Mr. Blanchard's letter was dated from the Island of Madeira.</s> <s sid="223" id="arma.c3.s223">He was out of health, and he had been ordered there by the doctors to try the climate.</s> <s sid="224" id="arma.c3.s224">His daughter was with him.</s> <s sid="225" id="arma.c3.s225">After heartily reciprocating all my mother's hopes and wishes, he proposed (if I intended leaving Barbadoes shortly) that I should take Madeira on my way to England, and pay him a visit at his temporary residence in the island.</s> <s sid="226" id="arma.c3.s226">If this could not be, he mentioned the time at which he expected to be back in England, when I might be sure of finding a welcome at his own house of Thorpe Ambrose.</s> <s sid="227" id="arma.c3.s227">In conclusion, he apologized for not writing at greater length; explaining that his sight was affected, and that he had disobeyed the doctor's orders by yielding to the temptation of writing to his old friend with his own hand.</s> </p>

    <p pid="76" id="arma.c3.p76" type="speech" form="extended" position="middle"><s sid="228" id="arma.c3.s228">"Kindly as it was expressed, the letter itself might have had little influence on me.</s> <s sid="229" id="arma.c3.s229">But there was something else besides the letter; there was inclosed in it a miniature portrait of Miss Blanchard.</s> <s sid="230" id="arma.c3.s230">At the back of the portrait, her father had written, half-jestingly, half-tenderly, <alt-qs/>'I can't ask my daughter to spare my eyes as usual, without telling her of your inquiries, and putting a young lady's diffidence to the blush.</s> <s sid="231" id="arma.c3.s231">So I send her in effigy (without her knowledge) to answer for herself.</s> <s sid="232" id="arma.c3.s232">It is a good likeness of a good girl.</s> <s sid="233" id="arma.c3.s233">If she likes your son--and if I like him, which I am sure I shall--we may yet live, my good friend, to see our children what we might once have been ourselves--man and wife.'<alt-qe/></s> <s sid="234" id="arma.c3.s234">My mother gave me the miniature with the letter.</s> <s sid="235" id="arma.c3.s235">The portrait at once struck me--I can't say why, I can't say how--as nothing of the kind had ever struck me before.</s> </p>

    <p pid="77" id="arma.c3.p77" type="speech" form="extended" position="end"><s sid="236" id="arma.c3.s236">"Harder intellects than mine might have attributed the extraordinary impression produced on me to the disordered condition of my mind at that time; to the weariness of my own base pleasures which had been gaining on me for months past, to the undefined longing which that weariness implied for newer interests and fresher hopes than any that had possessed me yet.</s> <s sid="237" id="arma.c3.s237">I attempted no such sober self-examination as this:</s> <s sid="238" id="arma.c3.s238">I believed in destiny then, I believe in destiny now.</s> <s sid="239" id="arma.c3.s239">It was enough for me to know--as I did know--that the first sense I had ever felt of something better in my nature than my animal self was roused by that girl's face looking at me from her picture as no woman's face had ever looked at me yet.</s> <s sid="240" id="arma.c3.s240">In those tender eyes--in the chance of making that gentle creature my wife--I saw my destiny written.</s> <s sid="241" id="arma.c3.s241">The portrait which had come into my hands so strangely and so unexpectedly was the silent messenger of happiness close at hand, sent to warn, to encourage, to rouse me before it was too late.</s> <s sid="242" id="arma.c3.s242">I put the miniature under my pillow at night; I looked at it again the next morning.</s> <s sid="243" id="arma.c3.s243">My conviction of the day before remained as strong as ever; my superstition (if you please to call it so) pointed out to me irresistibly the way on which I should go.</s> <s sid="244" id="arma.c3.s244">There was a ship in port which was to sail for England in a fortnight, touching at Madeira.</s> <s sid="245" id="arma.c3.s245">In that ship I took my passage."<qe/></s> </p><p pid="78" id="arma.c3.p78"><s sid="246" id="arma.c3.s246">Thus far the reader had advanced with no interruption to disturb him.</s> <s sid="247" id="arma.c3.s247">But at the last words the tones of another voice, low and broken, mingled with his own.</s> </p>

    <p pid="79" id="arma.c3.p79" type="speech"><s sid="248" id="arma.c3.s248"><qs/>"Was she a fair woman,"<qe/><sss/> asked the voice, <sse/><qs/>"or dark, like me?"<qe/></s> </p>

    </div>
    '''
    
    doc = StringDocument(data)
    rec = xmlp.process_document(session, doc)
    res = excl.process_record(session, rec)
    print etree.tostring(res[0])