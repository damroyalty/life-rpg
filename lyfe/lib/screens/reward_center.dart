import 'package:flutter/material.dart';

class RewardCenter extends StatelessWidget {
  const RewardCenter({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Map<String, dynamic>> rewards = [
      {
        'name': 'Doomscroll Socials',
        'cost': 100,
        'desc': '30 minutes of guilt-free social media time.',
      },
      {
        'name': 'Game Time',
        'cost': 200,
        'desc': 'Play your favorite game for 1 hour.',
      },
      {
        'name': 'Fast Food Treat',
        'cost': 300,
        'desc': 'Enjoy a fast food meal of your choice.',
      },
      {
        'name': 'Movie Night',
        'cost': 250,
        'desc': 'Watch a movie or binge a show episode.',
      },
      {
        'name': 'Lazy Morning',
        'cost': 150,
        'desc': 'Sleep in or lounge in bed for an extra hour.',
      },
      {
        'name': 'Shopping Spree',
        'cost': 500,
        'desc': 'Buy yourself something nice (within reason!).',
      },
      {
        'name': 'Sweet Treat',
        'cost': 120,
        'desc': 'Indulge in your favorite dessert.',
      },
      {
        'name': 'Takeout Dinner',
        'cost': 350,
        'desc': 'Order takeout from your favorite place.',
      },
      {
        'name': 'YouTube Binge',
        'cost': 100,
        'desc': 'Watch YouTube videos for 45 minutes.',
      },
      {
        'name': 'Coffee Shop Visit',
        'cost': 180,
        'desc': 'Relax at a coffee shop with your favorite drink.',
      },
    ];
    return Scaffold(
      appBar: AppBar(title: Text('Reward Center')),
      body: ListView.builder(
        itemCount: rewards.length,
        itemBuilder: (ctx, i) {
          return Card(
            margin: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
            child: ListTile(
              leading: Icon(Icons.card_giftcard, color: Colors.amberAccent),
              title: Text(
                rewards[i]['name'],
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              subtitle: Text(rewards[i]['desc']),
              trailing: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.monetization_on, color: Colors.amber, size: 18),
                  Text(' ${rewards[i]['cost']}'),
                ],
              ),
              onTap: () {
                showDialog(
                  context: context,
                  builder: (_) => AlertDialog(
                    title: Text('Reward Redeemed!'),
                    content: Text(
                      'You have redeemed the ${rewards[i]['name']}!',
                    ),
                    actions: [
                      TextButton(
                        child: Text('Nice!'),
                        onPressed: () => Navigator.pop(context),
                      ),
                    ],
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}
