# Set-Location "C:\Users\Theatina\Documents\Gdrive_ctkyl\Studies\Di_Master\Di_NLP\Courses\3rd_Semester\M913_Διαλογικά_Συστήματα_και_Φωνητικοί_Βοηθοί\Project\Rasa_Data"

if ( $args.Length -ne 0 )
{
    if ( $args[0] -eq "UniPal" -or $args[0] -eq "SocioPal" )
    {
        $domain = $args[0]
        Write-Output "graph path: .\data\my_graphs\$domain.html"
        rasa visualize -s ".\data\my_stories\$domain.yml" --out ".\data\my_graphs\$domain.html"

    }
    elseif ( $args[0] -eq "test") 
    {
        Write-Output "graph path: .\data\my_graphs\test_stories.html"
        rasa visualize -s ".\tests\test_stories.yml" --out ".\data\my_graphs\test_stories.html"
    }  
    else
    {
        Write-Output "ERROR: Unknown Dialogue System was given as argument! `n`nAvailable Dialogue Systems: `n1. UniPal`n2. SocioPal"
    }  
    
}
else
{
    Write-Output "ERROR: No arguments were given ! `n"
}


Write-Output " "