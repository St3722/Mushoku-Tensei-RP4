@echo off
echo ============================
echo Demarrage de Musko Tensei RP
echo ============================
echo.

:: Nettoyer les fichiers cache Python si nécessaire
if exist "modules\__pycache__" (
  echo Nettoyage des fichiers cache Python...
  del /Q /S "modules\__pycache__\*.*"
)

:: Lancer le jeu
echo Lancement du jeu...
python game_launcher.py

:: Si une erreur se produit
if %ERRORLEVEL% NEQ 0 (
  echo.
  echo Une erreur s'est produite lors de l'execution du jeu.
  echo Veuillez verifier que Python est bien installe.
  echo.
  pause
  exit /b 1
)

:: Fin normale
echo.
echo Fin de l'execution.
pause