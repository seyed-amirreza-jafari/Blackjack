from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import sys
import random

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		uic.loadUi('Blackjack.ui', self)

		self.dealer_1 = self.findChild(QLabel, 'dealer_1')
		self.dealer_2 = self.findChild(QLabel, 'dealer_2')
		self.dealer_3 = self.findChild(QLabel, 'dealer_3')
		self.dealer_4 = self.findChild(QLabel, 'dealer_4')
		self.dealer_5 = self.findChild(QLabel, 'dealer_5')

		self.player_1 = self.findChild(QLabel, 'player_1')
		self.player_2 = self.findChild(QLabel, 'player_2')
		self.player_3 = self.findChild(QLabel, 'player_3')
		self.player_4 = self.findChild(QLabel, 'player_4')
		self.player_5 = self.findChild(QLabel, 'player_5')

		self.shuffle_button = self.findChild(QPushButton, 'Shuffle_Button')
		self.add_card_button = self.findChild(QPushButton, 'Add_Card_Button')
		self.stand_button = self.findChild(QPushButton, 'Stand_Button')

		self.shuffle()

		self.shuffle_button.clicked.connect(self.shuffle)
		self.add_card_button.clicked.connect(self.add_player)
		self.stand_button.clicked.connect(self.stand)

		self.show()

	def stand(self):
		self.add_card_button.setEnabled(False)
		self.stand_button.setEnabled(False)

		if self.dealerScore >= 17:
			if self.dealerScore > 21:
				QMessageBox.about(self, 'Bust', 'Player won!')

			elif self.dealerScore == self.playerScore:
				QMessageBox.about(self, 'Tie', 'Tie!')

			elif self.dealerScore > self.playerScore:
				QMessageBox.about(self, 'Win', 'Dealer won!')

			else:
				QMessageBox.about(self, 'Win', 'Player won!')

		else:
			self.add_dealer()
			self.stand()

	def check_blackjack(self, player):
		if player == 'Player':
			if self.playerSpot == 2:
				if self.playerScore == 21:
					self.blacjack_status['Player'] = 'Yes'

			elif self.playerSpot >= 3:
				if self.playerScore == 21:
					self.blacjack_status['Player'] = 'Yes'

				elif self.playerScore > 21:
					for card_index, card in enumerate(self.player_cards):
						if card == 11:
							self.playerScore -= 10
							self.player_cards[card_index] = 1

					self.setWindowTitle(f'Dealer: {self.dealerScore} | Player: {self.playerScore}')

					if self.playerScore == 21:
						self.blacjack_status['Player'] = 'Yes'

					elif self.playerScore > 21:
						self.blacjack_status['Player'] = 'Bust'

		if player == 'Dealer':
			if self.dealerSpot == 2:
				if self.dealerScore == 21:
					self.blacjack_status['Dealer'] = 'Yes'

			elif self.dealerSpot >= 3:
				if self.dealerScore == 21:
					self.blacjack_status['Dealer'] = 'Yes'

				elif self.dealerScore > 21:
					self.blacjack_status['Dealer'] = 'Bust'

		if self.playerSpot == 2 and self.dealerSpot == 2:
			if self.blacjack_status['Dealer'] == 'Yes' and self.blacjack_status['Player'] == 'Yes':
				QMessageBox.about(self, 'Blackjack', 'Tie!')

				self.add_card_button.setEnabled(False)
				self.stand_button.setEnabled(False)

			elif self.blacjack_status['Dealer'] == 'Yes' and self.blacjack_status['Player'] == 'No':
				QMessageBox.about(self, 'Blackjack', 'Dealer won!')

				self.add_card_button.setEnabled(False)
				self.stand_button.setEnabled(False)

			elif self.blacjack_status['Dealer'] == 'No' and self.blacjack_status['Player'] == 'Yes':
				QMessageBox.about(self, 'Blackjack', 'Player won!')

				self.add_card_button.setEnabled(False)
				self.stand_button.setEnabled(False)

		elif self.playerSpot == 5:
			QMessageBox.about(self, '5 Cards', 'Player won!')

			self.add_card_button.setEnabled(False)
			self.stand_button.setEnabled(False)

		elif self.playerSpot >= 3:
			if self.blacjack_status['Dealer'] == 'Yes':
				QMessageBox.about(self, '21', 'Dealer won!')

				self.add_card_button.setEnabled(False)
				self.stand_button.setEnabled(False)

			elif self.blacjack_status['Player'] == 'Yes':
				QMessageBox.about(self, '21', 'Player won!')

				self.add_card_button.setEnabled(False)
				self.stand_button.setEnabled(False)

			elif self.blacjack_status['Player'] == 'Bust':
				QMessageBox.about(self, 'Bust', f'Player Lost: {self.playerScore}')

				self.add_card_button.setEnabled(False)
				self.stand_button.setEnabled(False)

	def shuffle(self):
		self.add_card_button.setEnabled(True)
		self.stand_button.setEnabled(True)

		suits = ['Clubs', 'Diamond', 'Hearts', 'Spades']
		values = range(1, 14)

		self.deck = list()

		for suit in suits:
			for value in values:
				self.deck.append(f'{suit}_{value}')

		self.dealer_cards = list()
		self.player_cards = list()

		self.dealerScore = 0
		self.playerScore = 0
		self.blacjack_status = {'Dealer': 'No', 'Player': 'No'}

		self.playerSpot = 0
		self.dealerSpot = 0

		self.dealer_1.clear()
		self.dealer_2.clear()
		self.dealer_3.clear()
		self.dealer_4.clear()
		self.dealer_5.clear()

		self.player_1.clear()
		self.player_2.clear()
		self.player_3.clear()
		self.player_4.clear()
		self.player_5.clear()

		self.add_dealer()
		self.add_dealer()

		self.add_player()
		self.add_player()

	def add_dealer(self):
		if self.dealerSpot < 5:
			try:
				card = random.choice(self.deck)

				if int(card.split('_')[1]) == 1:
					self.dealerScore += 11
					self.dealer_cards.append(11)
				elif int(card.split('_')[1]) == 11:
					self.dealerScore += 10
					self.dealer_cards.append(10)
				elif int(card.split('_')[1]) == 12:
					self.dealerScore += 10
					self.dealer_cards.append(10)
				elif int(card.split('_')[1]) == 13:
					self.dealerScore += 10
					self.dealer_cards.append(10)
				else:
					self.dealerScore += int(card.split('_')[1])
					self.dealer_cards.append(int(card.split('_')[1]))

				self.deck.remove(card)

				pixmap = QPixmap(f'J:/Programming/Python/GUI/Playing Cards/{card}.png')

				if self.dealerSpot == 0:
					self.dealer_1.setPixmap(pixmap)
					self.dealerSpot += 1

				elif self.dealerSpot == 1:
					self.dealer_2.setPixmap(pixmap)
					self.dealerSpot += 1

				elif self.dealerSpot == 2:
					self.dealer_3.setPixmap(pixmap)
					self.dealerSpot += 1

				elif self.dealerSpot == 3:
					self.dealer_4.setPixmap(pixmap)
					self.dealerSpot += 1

				elif self.dealerSpot == 4:
					self.dealer_5.setPixmap(pixmap)
					self.dealerSpot += 1

				self.setWindowTitle(f'Dealer: {self.dealerScore} | Player: {self.playerScore}')

				self.check_blackjack('Dealer')

			except Exception as e:
				QMessageBox.about(self, 'Game', str(e))
		
	def add_player(self):
		if self.playerSpot < 5:
			try:
				card = random.choice(self.deck)

				if int(card.split('_')[1]) == 1:
					self.playerScore += 11
					self.player_cards.append(11)
				elif int(card.split('_')[1]) == 11:
					self.playerScore += 10
					self.player_cards.append(10)
				elif int(card.split('_')[1]) == 12:
					self.playerScore += 10
					self.player_cards.append(10)
				elif int(card.split('_')[1]) == 13:
					self.playerScore += 10
					self.player_cards.append(10)
				else:
					self.playerScore += int(card.split('_')[1])
					self.player_cards.append(int(card.split('_')[1]))

				self.deck.remove(card)

				pixmap = QPixmap(f'J:/Programming/Python/GUI/Playing Cards/{card}.png')

				if self.playerSpot == 0:
					self.player_1.setPixmap(pixmap)
					self.playerSpot += 1

				elif self.playerSpot == 1:
					self.player_2.setPixmap(pixmap)
					self.playerSpot += 1

				elif self.playerSpot == 2:
					self.player_3.setPixmap(pixmap)
					self.playerSpot += 1

				elif self.playerSpot == 3:
					self.player_4.setPixmap(pixmap)
					self.playerSpot += 1

				elif self.playerSpot == 4:
					self.player_5.setPixmap(pixmap)
					self.playerSpot += 1
					
					self.add_card_button.setEnabled(False)
					self.stand_button.setEnabled(False)					

				self.setWindowTitle(f'Dealer: {self.dealerScore} | Player: {self.playerScore}')

				self.check_blackjack('Player')

			except Exception as e:
				QMessageBox.about(self, 'Game', str(e))

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
