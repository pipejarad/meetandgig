from django.core.management.base import BaseCommand
from django.utils import timezone
from usuarios.models import Invitacion


class Command(BaseCommand):
    help = 'Marca como expiradas las invitaciones que han superado su fecha límite'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecuta en modo simulación sin realizar cambios',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Buscar invitaciones pendientes que han expirado
        invitaciones_expiradas = Invitacion.objects.filter(
            estado='pendiente',
            fecha_expiracion__lt=timezone.now()
        )
        
        count = invitaciones_expiradas.count()
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'[DRY RUN] Se marcarían como expiradas {count} invitaciones'
                )
            )
            for invitacion in invitaciones_expiradas:
                self.stdout.write(
                    f'  - {invitacion.empleador.nombre_empresa} → {invitacion.musico.get_full_name()} '
                    f'({invitacion.oferta_laboral.titulo}) - Expiró: {invitacion.fecha_expiracion}'
                )
        else:
            # Marcar como expiradas
            for invitacion in invitaciones_expiradas:
                invitacion.marcar_como_expirada()
                self.stdout.write(
                    f'Expirada: {invitacion.empleador.nombre_empresa} → {invitacion.musico.get_full_name()} '
                    f'({invitacion.oferta_laboral.titulo})'
                )
            
            if count > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Se marcaron como expiradas {count} invitaciones'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('No hay invitaciones expiradas para marcar')
                )
