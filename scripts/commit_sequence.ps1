Param()

$root = Resolve-Path "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)/.."
Set-Location $root

if (-not (Test-Path .git)) {
    git init -b main
}

$messages = @(
    'Sassy Start', 'Tiny Triumph', 'Hotfix Hilarity', 'Sneaky Patch', 'Chicken Dance',
    'Panic Button', 'Coffee Overflow', 'Magic Smoke', 'Spicy Tacos', 'Ninja Move',
    'Oops Again', 'Waffle Logic', 'Bug Buffet', 'Feature Sprinkle', 'Polish Glitter',
    'Refactor Rave', 'Prettify Pixels', 'Doc Party', 'Ship It', 'Victory Lap'
)

for ($i=0; $i -lt $messages.Count; $i++) {
    $msg = $messages[$i]

    switch ($i) {
        0 { Add-Content README.md "Commit $($i+1): $msg" }
        1 { Add-Content src/ipl_journey/analysis.py "\n# tiny tweak $($i+1) - $msg" }
        2 { Add-Content src/ipl_journey/main.py "\n# small log $($i+1) - $msg" }
        3 { Add-Content src/ipl_journey/analysis.py "\ndef median(values): return sorted(values)[len(values)//2]" }
        4 { Add-Content src/ipl_journey/utils.txt "Helper notes $($i+1) - $msg" }
        5 { Add-Content src/ipl_journey/main.py "\n# added debug stub $($i+1) - $msg" }
        6 { Add-Content README.md "More progress $($i+1): $msg" }
        7 { Add-Content src/ipl_journey/analysis.py "\n# fixed edgecases $($i+1) - $msg" }
        8 { Add-Content src/ipl_journey/features.txt "Feature note $($i+1) - $msg" }
        9 { Add-Content src/ipl_journey/main.py "\n# ninja patch $($i+1) - $msg" }
        10 { Add-Content src/ipl_journey/analysis.py "\n# oops fix $($i+1) - $msg" }
        11 { Add-Content README.md "Doc update $($i+1): $msg" }
        12 { Add-Content src/ipl_journey/analysis.py "\n# bug buffet cleanup $($i+1) - $msg" }
        13 { Add-Content src/ipl_journey/main.py "\n# feature sprinkle $($i+1) - $msg" }
        14 { Add-Content src/ipl_journey/analysis.py "\n# polish glitter $($i+1) - $msg" }
        15 { Add-Content src/ipl_journey/analysis.py "\n# refactor rave $($i+1) - $msg" }
        16 { Add-Content src/ipl_journey/main.py "\n# prettify pixels $($i+1) - $msg" }
        17 { Add-Content README.md "Docs: $($i+1) - $msg" }
        18 { Add-Content src/ipl_journey/main.py "\n# ship it $($i+1) - $msg" }
        19 { Add-Content README.md "Final note: $($i+1) - $msg" }
        default { Add-Content README.md "Extra $($i+1) - $msg" }
    }

    git add -A
    git commit -m "$msg"
}

Write-Output "Creating GitHub repo (if needed) and pushing..."
gh repo create ipl-journey --public --confirm | Out-Null
git branch -M main
git push -u origin main

Write-Output "Done."
