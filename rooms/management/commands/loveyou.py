from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "This command tells me that he loves me"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times",
            help="How many times do you want me to tell you that I love you?",
        )

    def handle(self, *args, **options):

        print(args, options)

        times = int(options.get("times"))

        for i in range(0, times):
            # print("I love you")
            self.stdout.write(self.style.SUCCESS("I love you"))
