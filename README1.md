README1

_HTML STYLING_____________________________________________________________________________________________________________________________

<p style="
    font-family: Arial, sans-serif;
    font-style: italic;
    font-size: 18px;
    color: darkgreen;
    background-color: #f0f0f0;
    border: 2px dashed green;
    padding: 12px;
    margin: 20px;
    line-height: 1.6;
    text-transform: capitalize;
    letter-spacing: 1px;
    text-shadow: 1px 1px 2px lightgray;
    box-shadow: 3px 3px 5px #ccc;
    Text-align: center;
    cursor: pointer;
    text-indent: 40px;
">
    This paragraph demonstrates various inline styling properties including text indent, 
    borders, padding, margin, line height, and more. The first line of this paragraph 
    begins with a 40px indent..
</p>

- Underline with                <u> xxxx </u> inside the p-tag
- vHighlight with               <span class="highlight-text">This is highlighted text</span> inside the p-tag
- Borders: Add borders 

  around the paragraph          border: 1px solid black;  or any style/color.
                            
- Padding and margin:           padding: 10px 
  Control spacing padding       argin: 10px;
  inside  & margin outside      

- Line height: Adjust s         line-height: 1.5; 
  pacing between lines with  
                            
- Text transform: Change        text-transform: uppercase;  or  capitalize .
  case with  
                            
- Letter spacing and            Use letter-spacing:   and  word-spacing  to adjust 
  word spacing:                 spacing between letters or words.
                            
- Text shadow:                  Add shadow to text with  text-shadow: 2px 2px 3px gray; .
- Opacity:                      Make paragraph partially transparent, e.g.  opacity: 0.7; .
- Box shadow:                   Apply shadow around the paragraph box with  box-shadow .
- Cursor:                       Change mouse cursor style on hover with  cursor: pointer; .
- White-space handling:         Control whether to collapse whitespace or wrap with  white-space .

  <p class="inline">            Display inline - flows with text, no new line.</p>
  <span>--</span>               This text is on the same line as the inline paragraph.</span>
  <p class="none">              You should not see this paragraph (display: none).</p>

                                <span> element can be placed inside a <p> tag. A <span> 
                                element can have all the inline styling that a  <p>  element 
                                can have. Some CSS properties related to block layout (like  
                                margin-top , margin-bottom , or  width ,  height ) may not 
                                behave as expected on a  <span>  because it 
                                doesn’t create a block box by default. For purely   
                                text-related styles—such as  font-family ,  
                                font-size ,  font-weight  (bold),  font-style  (italic),    
                                text-decoration  (underline), color , background-color ,  
                                text-align  (when applied to a block   container parent),  
                                letter-spacing ,   line-height , text-shadow ,  opacity , 
                                and many more— <span> handles them just like  <p>  does.

This is line one.<br><br><br>   This is line two after three line breaks blanks.
  
_BULLETS___________________________________________________________________________________________________________________________________

  &bull;                        First point in a bulleted line<br>
  &bull;                        Second bullet with more information<br>
  &bull;                        Third item continues in normal paragraph flow

Adds three bullet points as plain-text symbols ( -  ). Each line is broken using  <br>  for 
line breaks

_URL LINKS_________________________________________________________________________________________________________________________________

This is a paragraph with a 
  <a href="https://www.example.com">link to Example.com</a> 
  inside it.
  Go to the <a href="#section2">second section</a> of this page.
  Go to the <a href="#section2">second section</a> of this page. Where there is a <p id="section2"> S
  omewhere in the document. 

  In the .md file do this...
  [Image Src...](https://www.wikiart.org/en/pablo-picasso/friendship-1908)

  for reference / image  links use 
<p style="font-size: 0.4em;">[Image Src...](url)</p>

_IMAGE OPTIONS_____________________________________________________________________________________________________________________________

Image Syntax Options: ![[ filename | description | size | alignment ]]
1. ![[image]]                                   - Just filename
2. ![[image | My description]]                  - Filename + description
3. ![[image | | 300px]]                         - Filename + size (no description)
4. ![[image | | 50%]]                           - Filename + percentage size
5. ![[image | | 400x300]]                       - Filename + dimensions
6. ![[image | | 400]]                           - Filename + auto-px size
7. ![[image | | | center]]                      - Filename + alignment only
8. ![[image | | | left]]                        - Filename + left alignment
9. ![[image | | | right]]                       - Filename + right alignment
10. ![[image | Description | 300px]]            - Filename + description + size
11. ![[image | Description | 50%]]              - Filename + description + percentage
12. ![[image | Description | 400x300]]          - Filename + description + dimensions
13. ![[image | Description | 400]]              - Filename + description + auto-px
14. ![[image | Description | | center]]         - Filename + description + alignment
15. ![[image | Description | | left]]           - Filename + description + left align
16. ![[image | Description | | right]]          - Filename + description + right align
17. ![[image | | 300px | center]]               - Filename + size + alignment
18. ![[image | | 50% | left]]                   - Filename + percentage + left align
19. ![[image | | 400x300 | right]]              - Filename + dimensions + right align
20. ![[image | | 400 | center]]                 - Filename + auto-px + alignment
21. ![[image | Description | 300px | center]]   - All parameters: centered
22. ![[image | Description | 300px | left]]     - All parameters: left aligned
23. ![[image | Description | 300px | right]]    - All parameters: right aligned
24. ![[image | Description | 50% | center]]     - All: percentage + centered
25. ![[image | Description | 400x300 | left]]   - All: dimensions + left
26. ![[image | Description | 400x300 | right]]  - All: dimensions + right
Size Options:
* 300px - Fixed pixels
* 50% - Percentage width
* 400x300 - Width × Height
* 400 - Auto-convert to pixels
Alignment Options:
* center - Centered
* left - Left aligned, text wraps right
* right - Right aligned, text wraps left
text pop-up when hover or click
All parameters are optional except the filename! Use empty | placeholders to skip parameters.

_REPLACEMENTS_____________________________________________________________________________________________________________________________
  NEWPLAGE 
  <div style="break-after: page;"></div><br>                                                          <NEWPAGE> 
  
  TITLE
  <p style="color: #f09e5a;"><span class="highlight-text">xxx</span></p>xxx</span></p>              <TITLE="xxx">
    FIND: <\s*p\s+style\s*=\s*["']color:\s*[^"']*["']\s*>\s*<\s*span\s+class\s*=\s*["'][^"']*["']\s*>\s*(.*?)\s*<\s*\/span\s*>\s*<\s*\/p\s*>.*  
    REPLACE: <TITLE="$1">
  
  SOURCE
  <p style="text-align: center; font-size: 0.4em;">[Image Src...](xxx)</p>                            <SOURCE="xxx">
    FIND: <\s*p\s+style\s*=\s*["'][^"']*text-align\s*:\s*[^"';]*;?\s*[^"']*font-size\s*:\s*[^"';]*;?\s*[^"']*["']\s*>\s*\[\s*Image\s+Src\s*\.\.\.\s*\]\s*\((.*?)\)\s*<\s*\/p\s*>
    REPLACE: <SOURCE="$1">    

  CHAPTER
  ## xxx xxx                                                                                          <CHAPTER="xxx xxx">
    FIND: ^\s*##\s+(.*)$
    REPLACE: <CHAPTER="$1">

  PAGE END MARKER
  <p style="text-align: center; font-style: bold;"> xxx</p>                                           <PAGE END MARKER="xxx">
    FIND:<\s*p\s+style\s*=\s*["'][^"']*text-align\s*:\s*center\s*;?[^"']*font-style\s*:\s*bold\s*;?[^"']*["']\s*>\s*(.*?)\s*<\s*\/p\s*>
    REPLACE: <PAGE END MARKER="$1">

  ///                         Comment line - Delete to the end of the line
  From //* to *//             comment parapgh - Delete Between 
  **text** or __text__        Remove BOLD
  ==text==                    Remove Highlight
  *text* or _text_            Remove Itlalics
  <u>text</u>                 Remove bullets
  <em>text</em>               Remove Emphasis
  [text] (URL)                <a href="url>test</a>                                 (HTML LINK)
  <NEWPAGE>                   <div style="break-after: page;"></div><br>
  <TITLE="xxx">               <p style="color: #f09e5a;"><span class="highlight-text">xxx</span></p>xxx</span></p>
  <SOURCE="xxx">              <p style="text-align: center; font-size: 0.4em;">[Image Src...](xxx)</p>. also allow 
  <CHAPTER="xxx">             ## xxx also support 'xxx' there will be a space between ## and xxx
  <IMAGE="xxx">               ![[xxx]] and also support 'xxx'
  <PAGE END MARKER="xxx">     <p style="text-align: center; font-style: bold;"> xxx</p> ignore space and also support 
  <FOOTER="xxx">              <p style="font-size: 0.4em;">xxx</p>                                          (Paragraph Tiny footer)


_PAGE HANDLING_____________________________________________________________________________________________________________________________

  Anything above this is ignored.This is goels on top of the file
  <STARTPAGE> / <NEWPAGE>
  <CHAPTER="1"> 
  <IMAGE="xxx">
  <TITLE="xxx"> 

    Paragraphs............

  <DPosition=":[ walign |talign | fstyle] xxx">
  <PAGE END MARKER="xxx"> 
  <ENDPAGE> / <NEWPAGE>

_General Items_____________________________________________________________________________________________________________________________
Item                                                Description
___________________________________________________________________________________________________________________________________________
<footer="xxx">                                      A <span> element with no positioning. Can be wrapped by a <DPosition>                             
<source="Label", "URL">                             A <span> Element with no positioning can be wrapped by a <DPosition>  
<PAGE END MARKER="~***~">                           A <p> element centered to parent
<FIRSTPAGE><NEWPAGE><LASTPAGE>                      <div style="break-after: page;"></div><br>
<CHAPTER="Chapt_name">                              Converts to ## Chapt_name and then processed with styling and TOC insertion.
<IMAGE="xxx">                                       Converts ![[xxx]] (xxx is a tring with | separated image attributes - see below)
<TITLE="xxx">                                       A <p> element with no positioning, but has color and styling
___________________________________________________________________________________________________________________________________________

_DPosition - Indenting_____________________________________________________________________________________________________________________
<DPosition=":[ walign |talign | fstyle] xxx"> OR <DPostion=":[ | | ] xxx"> Supports both pipe and comma
Parameter	  Purpose	                  Allowed Values	                      Default (if empty)	    CSS Generated
___________________________________________________________________________________________________________________________________________
walign	    Sets horizontal margin    "left", "right", "center", "both"     No margin rule          margin-left: 8%; margin-right: 8%;
            (indentation/centering)	  or empty                                                      margin-left: auto; margin-right: auto;
                                                                                                    margin-left: 8%; margin-right: 8%;
                                                                                                    (empty → no rule)		

talign	    Aligns text inside the    "left", "right", "center", or empty	  "left"                  text-align: left; text-align: 
            element	                                                                                right; text-align: center;

fstyle	    Font style(italic/normal)	"italic", "normal", or empty	        "normal"	              font-style: italic; font-style: normal;

content	    The inner text or HTML	  any string (may contain HTML tags)    (required)	            Placed as the content of the <div>
___________________________________________________________________________________________________________________________________________ 
Important notes:
Examples of usage:

<DPosition=":[left|center|italic]Some text">
→ <div style="margin-left: 8% !important; text-align: center !important; font-style: italic !important;">Some text</div>
<DPosition=":[both|right|normal]Another text">
→ <div style="margin-left: 8% !important; margin-right: 8% !important; text-align: right !important; font-style: normal !important;">Another text</div>
<DPosition=":[center||]Centered only">
→ <div style="margin-left: auto !important; margin-right: auto !important; text-align: left !important; font-style: normal !important;">Centered only</div>
<DPosition=":[| | ]Plain text">
→ <div style="text-align: left !important; font-style: normal !important;">Plain text</div>

_Tool-Tips_________________________________________________________________________________________________________________________________
:[floatright]     – trigger floats right, with a right margin of 8%.
:[floatleft]      – trigger floats left, with a left margin of 8%.
:[floatcenter]    – trigger is centered (block with auto margins).
inline            - not present

_Tooltip & tiptext position___________________________________________________________________________________________________
Position    Parameter	  Purpose	                                        Default                   
______________________________________________________________________________________________________________________________
floatmarker
1           T →         data-top                                        5.5vh
2           L →         data-left                                       6.5vw
3           BG →        data-bottom-gap                                 0vh
4           H →         data-height                                     var(--tt-max-height) (91vh desktop)
5           W →         data-width                                      var(--tt-max-height) (91vh desktop)
6           MH →        data-maxheight                                  var(--tt-max-height) (91vh desktop)
7           MW →        data-maxwidth                                   var(--tt-max-height) (91vh desktop)
10          loc →       data-position                                   "bottom-left"
11          tloc →      data-textalign                                  "left"
_USAGE_____________________________________________________________
<ttt-LEXTIP=":[floatxxxt]word", ":[ Top | left | Bottom-gap | Height | Width | MaxHeight| Maxwidth | LOC | TLOC ]tip"> 
<ttt-LEXTIP=":[floatleft]Click word", ":[ @| | | | | | | | left]Your tooltip text here"><br> (fullheight and full width)
Supports both Pipe and commna
___________________________________________________________________________________________________________________________________________
Attribute	          Purpose	                          Example Values (all labels are case censitive)
___________________________________________________________________________________________________________________________________________
data-position	      Defines how the tooltip           center-height   – centers tooltip vertically (viewport then clamped to page)
                    is positioned relative            center-width    – centers horizontally
                    to the trigger and the            center-both     – centers both axes
                    viewport/page.                    bottom-page     – places tooltip at the bottom left of the page with a gap but uses
                                                                         Data.Left to position horizontally
                                                      bottom-left     – places tooltip at the bottom left of the page with a gap
                                                      bottom-center   – CENTERS the  tooltip at the bottom left of the page with a gap
                                                      bottom-right    – places tooltip at the bottom left of the page with a gap
                                                      fixed (default) – uses explicit top/left/bottom/right values relative to viewport
                                                                        TOP center -> data-left = center & data-position = fixed 
                                                                        Center-Center -> data-left= center, data-top=center, data-position=fixed
                                                      absolute        - The tooltip is positioned using the top/bottom and left/right 
                                                                          values you provide (or defaults). No special layout adjustments 
                                                                          are made   
                                                                                      
_________________________________________________________________________________________________________________________________________
data-top          @             Width is forced to 50 vw (half the viewport width). Max‑height is forced to 3 em (content scrolls 
                                if longer).These dimensions are applied with !important to override any CSS classes.The tooltip’s height 
                                is set to auto so it only grows as needed, up to the max‑height. Left if trigger center < 25 vw → tooltip’s 
                                left edge is 5 vw from the left viewport edge. Center if trigger center between 25 vw and 75 vw → tooltip 
                                is horizontally centered in the viewport. Right if trigger center > 75 vw → tooltip’s right edge is 5vw 
                                from the right viewport edge.
_________________________________________________________________________________________________________________________________________
	                Sets the tooltip’s position       
data-top          relative to the viewport or 
data-bottom       page. Can be CSS lengths 
data-left         (e.g., 10vh, 20px, 50%) or          "10vh", "20px", "50%", "@"
data-right        the special value "@" which 
                  snaps the corresponding edge 
                  to the same edge of the 
                  trigger  element.	
                  data-left supports center
___________________________________________________________________________________________________________________________________________
data-bottom-gap	  Only used with data-position
                  ="bottom-page". Adds a gap 
                  between the tooltip’s bottom        "2vh", "10px"
                  edge and the bottom of the 
                  page (or viewport).	
___________________________________________________________________________________________________________________________________________
data-animation	  Chooses the tooltip’s               "fade" (default), "bounce", "slide", "zoom"
                  entrance/exit animation.	
___________________________________________________________________________________________________________________________________________
data-textalign	  Aligns the tooltip text             "left" (default), "center", "right"
                  inside the tooltip box.	
___________________________________________________________________________________________________________________________________________
data-tiptext	    The actual tooltip 
                  content (HTML allowed,              any string (e.g., "This is a tooltip")
                  escaped by JavaScript).	                  
___________________________________________________________________________________________________________________________________________ 
Attribute	        Purpose	Example Values	Notes
data-width	      Explicit width of tooltip          "300px", "50vw", "auto" (default)	      Overrides any CSS class that sets width.
data-height	      Explicit height of  tooltip        "200px", "30vh", "auto"	                Overrides any CSS class that sets height.
data-maxwidth	    Maximum width of tooltip           "400px", "80vw"	                        Restricts width when content would exceed it. 
                    	                                                                        Works alongside data-width.
data-maxheight	  Maximum height of tooltip         "300px", "50vh"	                          Restricts height; if content overflows, 
                                                                                              scrollbars appear.
_Supports_ pixels: "300px", Percentages: "50%" (relative to the containing block), Viewport units: "50vw", "30vh", Other CSS units: "20em",
 "10rem", "auto", etc. Important: _Do not use a bare number_ without a unit (e.g., "300"), as that would be invalid CSS
___________________________________________________________________________________________________________________________________________ 
Important notes:

-   center-height – The tooltip is vertically centered within the page content area (or viewport if no .page is found). Any data-top value is ignored.
-   center-width – The tooltip is horizontally centered within the page content area (or viewport). Any data-left value is ignored.
-   center-both – Both vertical and horizontal centering are applied; data-top and data-left are ignored.
-   The "@" value for edges only works when the tooltip’s data-position is not one of the special modes (center-*, bottom-page). In those 
    modes, "@" is ignored for that axis because the mode overrides it.
-   The bottom-page mode uses data-bottom-gap to separate the tooltip from the bottom of the page. The gap value can be in vh or px.
-   The centering modes (center-*) first try to place the tooltip at the viewport center, then clamp it to keep it inside the page 
    (with a 10 px margin). This ensures the tooltip never goes off‑screen.
-   The center-* modes can be combined with data-top/data-left/data-bottom/data-right to provide fallback vertical/horizontal positions 
    if clamping moves the tooltip. For example, center-width uses the given top value (or bottom) for vertical placement, while the 
    horizontal position is centered.

_Standard ToolTip Inventory_________________________________________________________________________________________________________________
<span class="tooltip-trigger" 
  data-top="5.5vh"   data-left="6.5vw"    data-height="20vh"   data-width="60vw"  data-animation="ZOOM"   
  data-tiptext="📌 ToolTip placed at Top and Bottom with Heightand Width, fading in "
  data-position="fixed">A Clickable word
</span>


Triming logic
--------------------------------------------------------------------------------------------------
  1. Get the page’s bounding rectangle relative to the viewport (pageRect).

  2. Define an inner padding (innerPadding = 10px) to keep the tooltip away from the page edges.

  3. Convert the final top, left, height, width strings to pixel numbers (using toPixels).
        - If a value cannot be converted (e.g., calc()), that axis is skipped.

  4. Compute total dimensions including the tooltip’s fixed padding/border (extra = 22px = 10px top/bottom padding + 1px top/bottom border × 2).
        - totalWidth = widthPx + extra (if widthPx is valid)
        - totalHeight = heightPx + extra (if heightPx is valid)

  5. Clamp top and left so the tooltip’s outer box stays inside the page:
        - minTop = pageRect.top + innerPadding
        - maxTop = pageRect.bottom - totalHeight - innerPadding
        - If newTop < minTop, set to minTop; if newTop > maxTop, set to maxTop.
        (Similarly for left with minLeft / maxLeft.)

  6.fter repositioning, trim width/height if still overflowing:
        - Right edge overflow: availableWidth = pageRect.right - leftPx - innerPadding. If totalWidth > availableWidth, reduce content width:
          newContentWidth = max(0, availableWidth - extra) → update width (as a pixel string).
        - Bottom edge overflow: availableHeight = pageRect.bottom - topPx - innerPadding. If totalHeight > availableHeight, reduce content height similarly.
          Updated top, left, height, width strings (with px units) are then passed to toggleTooltip.

Summary:
      ✅  data-top="@" data-left="@"  → Below clickable word, perfectly centered and Boundary Safe
          left, right and bottom
      ✅  data-top="center" data-left="center"  → Screen center
      ✅  Fixed positioning ( "30", "30%", "30px" ,  "10vh" , "calc(mixed_arithmentic)" )
      ✅  All animations (fade, bounce, slide, zoom) - DOn ont use....
      ✅  Text alignment ( data-textalign="center|right|left" )
      ✅  Responsive sizing (mobile/tablet/desktop)

 --------------------------------------------------------------------------------------------------




_END_______________________________________________________________________________________________________________________________________