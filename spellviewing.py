from py_stealth import *

def train_spellviewing():
    target_skill = 120

    # Meditate to regain mana
    

    while GetSkillValue('Spellweaving') < target_skill:

        while GetMana(Self()) < GetMaxMana(Self()) * 0.3:  # Meditate if below 30% mana
            UseSkill('Meditation')
            Wait(10000)  # Wait 10 seconds while meditating    

        # Check health and heal if needed
        while GetHP(Self()) < GetMaxHP(Self()) * 0.7:  # Heal if below 70% HP
            Cast('Greater Heal')
            WaitTargetSelf()
            # Wait(1000)


        # Cast spellviewing on self
        Cast('Word of Death')
        WaitTargetSelf()
        # Wait(1000)
        
        
        
        
        
        # Wait a bit before next iteration
        # Wait(1000)
    
    print("Spellweaving training complete!")

# Start the training
train_spellviewing()

